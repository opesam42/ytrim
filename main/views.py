from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from .utils import Video
import urllib.parse
import os


# Create your views here.
def index(request):

    if request.method == 'POST':
        videoUrl = request.POST.get('ylink')
        trimStart = request.POST.get('s-time')
        trimEnd = request.POST.get('e-time')
        #create an instance of the Video class
        video = Video(videoUrl)
        
        videoTitle = video.getTitle()[0] #get title
        ytChannel = video.getTitle()[1] #get youtube channel
        thumbnailUrl = video.getThumbnail() #get thumbnail image
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
