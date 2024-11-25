from django.conf import settings
from .misc import Misc
from pytubefix import YouTube
from pytubefix.cli import on_progress
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
from dotenv import load_dotenv

load_dotenv()

# https://github.com/JuanBindez/pytubefix/issues/226 for generating token easily
# https://www.npmjs.com/package/youtube-po-token-generator npm package for automating youtube po-token

class Video:
    def __init__(self, url):
        self.url = url
        self.output_path = os.path.join(settings.MEDIA_ROOT, "downloads/")

        # for pytube download without bot intervention
        self.po_token = os.getenv("PO_TOKEN")
        self.visitor_data = os.getenv("VISITOR_DATA")

    def verifier(self):
        po_token = os.getenv("PO_TOKEN")
        visitor_data = os.getenv("VISITOR_DATA")
        return po_token, visitor_data

    def getTitle(self):
        try:
            yt = YouTube( self.url, on_progress_callback=on_progress, use_po_token=True, token_file=os.path.join(settings.MEDIA_ROOT, "file.json") )
            video_title= yt.title
            return video_title
                
        except Exception as e:
            print(str(e))
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

        
