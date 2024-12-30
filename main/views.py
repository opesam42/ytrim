from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse
from .utilities.youtubeDownload import Video
# from .utilities.youtube2 import Video
# from .utilities.ytD import Video
from .utilities.deleteFile import deleteFiles
import urllib.parse
import os
import requests



# Create your views here.
def index(request):
    # delete files that are have been downloaded more than an hour ago
    output_path = os.path.join(settings.MEDIA_ROOT, "downloads/")
    if os.path.exists(output_path):
        files = os.listdir(output_path)  #return list of downloaded files
        if files:
            for file in files:
                try:
                    print(f'Checking {file}')
                    file = os.path.join(output_path, file)
                    deleteFiles(file, 60) #delete file which stay longer than 60 minutes
                except:
                    print(f'Error checking {file}')
                    continue
        else: 
            print('No file in download to check')
    else:
        print('Download directory does not exist')

    if request.method == 'POST':
        videoUrl = request.POST.get('ylink')
        trimStart = request.POST.get('s-time')
        trimEnd = request.POST.get('e-time')
        #create an instance of the Video class
        video = Video(videoUrl)

        print(f'Downloading video')
        
        # trim video and get link
        if(trimStart=="") and (trimEnd==""):
            download_link = video.download()
        else:
            if(':' in trimStart) and (':' in trimEnd):
                download_link = video.trim(trimStart, trimEnd) #for HH:MM:SS format
            else:
                download_link = video.trim( int(trimStart), int(trimEnd) ) #for seconds only format

        encoded_link = urllib.parse.quote(download_link)
        return redirect(f'download?link={encoded_link}')

    
    return render(request, 'main/index.html', {
        'API_KEY': settings.API_KEY,
    })

def download(request):
    download_link = request.GET.get('link')
    if download_link:
        decoded_link = urllib.parse.unquote(download_link)
        filename = os.path.basename(decoded_link)

        return render(request, 'main/download.html', {
            'downloadURL': download_link,
            'filename': filename,
            'MEDIA_URL': settings.MEDIA_URL,
            })
    else:
        return redirect(index)
    
def youtube_api(request):
    video_id = request.GET.get('videoId')
    if not video_id:
        return JsonResponse({'error': 'No videoid provided'}, status=400)

    api_key = settings.API_KEY
    url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={video_id}&key={api_key}' 
    
    response = requests.get(url)
    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse({'error': 'Failed to fetch video details'}, status=500)
