from django.conf import settings
from .misc import Misc
# from .selenium import fetchPageWithHeaders
from pytubefix import YouTube
from pytubefix.cli import on_progress
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
# from requests import get
import requests
from dotenv import load_dotenv
import asyncio
 

load_dotenv()

# https://github.com/JuanBindez/pytubefix/issues/226 for generating token easily
# https://www.npmjs.com/package/youtube-po-token-generator npm package for automating youtube po-token

class Video:
    def __init__(self, url):
        self.url = url
        self.output_path = os.path.join(settings.MEDIA_ROOT, "downloads/")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Referer': 'https://www.youtube.com/',
        }

    

    def getTitle(self):
        try:
            
            yt = YouTube( self.url, on_progress_callback=on_progress, use_po_token=True, token_file=os.path.join(settings.MEDIA_ROOT, "file.json") )
            video_title= yt.title
            return video_title
                
        except Exception as e:
            print(f'title not found: {str(e)}')
            return "Not working"
        
    def download(self):
        

        # output_path = os.path.join(settings.MEDIA_ROOT, "downloads/")
        misc = Misc()
        custom_name = misc.sanitize_filename( self.getTitle() )

        try:

            yt = YouTube( self.url, on_progress_callback=on_progress, use_po_token=True, token_file=os.path.join(settings.MEDIA_ROOT, "file.json") )
            stream = yt.streams.get_highest_resolution()
            video_file = stream.download( output_path = self.output_path)
            return video_file

            
        except Exception as e:
            print(f'Error during video download: {str(e)}')
            print(os.path.join(self.output_path))


    def trim(self, start, end):
        # video = os.path.join(settings.MEDIA_ROOT, "downloads/", "20-Sec-Timer.mp4")
        video = self.download()
        misc = Misc()
        custom_name = misc.sanitize_filename( self.getTitle() )

        if os.path.exists(video):
            print(f'{video} found')
        else:
            print("Not found")
        
        extension = misc.get_file_extension(video) #get extension of file
        output_file = os.path.join(settings.MEDIA_ROOT, "downloads/", custom_name + '_trimmed' + extension)

        try:
            with VideoFileClip(video) as clip:
                clip = clip.with_subclip(start, end)
                clip.write_videofile(
                    output_file, 
                    codec="libx264",
                    audio_codec='aac'
                )
        except Exception as e:
            print(f'Error trimming: {str(e)}')

        os.remove(video) #delete original video after trimming

        return output_file

        
