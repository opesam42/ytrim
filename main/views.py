from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from .utilities.youtubeDownload import Video
from .utilities.deleteFile import deleteFiles
import urllib.parse
import os


# Create your views here.
def index(request):

    # delete files that are have been downloaded more than an hour ago
    output_path = os.path.join(settings.MEDIA_ROOT, "downloads/")
    files = os.listdir(output_path) #return list of downloaded files
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

    if request.method == 'POST':
        videoUrl = request.POST.get('ylink')
        trimStart = request.POST.get('s-time')
        trimEnd = request.POST.get('e-time')
        #create an instance of the Video class
        video = Video(videoUrl)
        
        # metaData = video.getTitle()
        # videoTitle = metaData[0] #get title
        # ytChannel = metaData[1] #get youtube channel
        # thumbnailUrl = metaData[2] #get thumbnail image
        videoTitle = 'hello'
        ytChannel = 'hello'
        thumbnailUrl = 'hello'
        print(f'Downloading {videoTitle}')
        print(f'thumbnail image {thumbnailUrl}')
        
        # trim video and get link
        if(trimStart=="") and (trimEnd==""):
            download_link = video.download()
        else:
            if(':' in trimStart) and (':' in trimEnd):
                download_link = video.trim(trimStart, trimEnd) #for HH:MM:SS format
            else:
                download_link = video.trim( int(trimStart), int(trimEnd) ) #for seconds only format

        encoded_link = urllib.parse.quote(download_link)
        return redirect(f'download?link={encoded_link}&videoTitle={videoTitle}&ytChannel={ytChannel}&thumbnail={thumbnailUrl}')

    
    return render(request, 'main/index.html')

def download(request):
    download_link = request.GET.get('link')
    if download_link:
        decoded_link = urllib.parse.unquote(download_link)
        filename = os.path.basename(decoded_link)

        # get other parameters
        videoTitle = request.GET.get('videoTitle')
        ytChannel = request.GET.get('ytChannel')
        thumbnailUrl=request.GET.get('thumbnail')
        return render(request, 'main/download.html', {
            'downloadURL': download_link,
            'filename': filename,
            'MEDIA_URL': settings.MEDIA_URL,

            'videoTitle':videoTitle,
            'ytChannel': ytChannel,
            'thumbnailUrl': thumbnailUrl,
            })
    else:
        return redirect(index)
