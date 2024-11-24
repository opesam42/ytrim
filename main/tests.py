from django.test import TestCase
from django.conf import settings
import os
from pytubefix import YouTube
from pytubefix.cli import on_progress


def download():
    try:
        yt = YouTube( "https://youtu.be/1aA1WGON49E?si=ennN790mLT26NXQW", on_progress_callback=on_progress )
        print(yt.title)
        stream = yt.streams.get_highest_resolution()
        video_file = stream.download( output_path = os.path.join(settings.MEDIA_ROOT, "downloads/") )
        return video_file
        
    except Exception as e:
        print(f'Error during video download: {str(e)}')
        print( os.path.join(os.path.join(settings.MEDIA_ROOT, "downloads/")) )

download()