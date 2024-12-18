from django.conf import settings
from .helper_func import sanitize_string, get_file_extension, get_file_name_no_extension
import ffmpeg
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
# from requests import get
import requests
from dotenv import load_dotenv

load_dotenv()

# https://github.com/JuanBindez/pytubefix/issues/226 for generating token easily
# https://www.npmjs.com/package/youtube-po-token-generator npm package for automating youtube po-token

class Video:
    def __init__(self, url):
        self.url = url
        self.output_path = os.path.join(settings.MEDIA_ROOT, "downloads/")

    def youtubeLib(self):
        return YouTube( 
            self.url,
            on_progress_callback=on_progress,
            use_po_token=True,
            token_file=os.path.join(settings.MEDIA_ROOT, "file.json")
        )

    def getTitle(self):
        try:
            yt = self.youtubeLib()
            video_info = [yt.title, yt.author]
            return video_info
                
        except Exception as e:
            print(str(e))
            return "Not working"

    def getThumbnail(self):
        yt = self.youtubeLib()
        thumbnail = yt.thumbnail_url.replace('default.jpg', 'hqdefault.jpg')
        return thumbnail
        
        
    def download(self):
        # output_path = os.path.join(settings.MEDIA_ROOT, "downloads/")
        video_title = 'title'
        custom_name = sanitize_string( video_title )

        try:
            yt = self.youtubeLib()
            stream = yt.streams.get_highest_resolution()
            video_file = stream.download( output_path = self.output_path)
            return video_file
            
        except Exception as e:
            print(f'Error during video download: {str(e)}')
            print(os.path.join(self.output_path))


    def trim(self, start, end):
        # video = os.path.join(settings.MEDIA_ROOT, "downloads/", "20-Sec-Timer.mp4")
        video = self.download()
        video_title = get_file_name_no_extension(video) #extract filename discarding the path and extension
        # video_title = self.getTitle()[0]
        custom_name = sanitize_string( video_title )

        if os.path.exists(video):
            print(f'{video} found')
        else:
            print("Not found")
        
        extension = get_file_extension(video) #get extension of file
        output_file = os.path.join(settings.MEDIA_ROOT, "downloads/", custom_name + '_trimmed' + extension)

        try:
            duration = end - start
            ffmpeg.input(video, ss=start, t=duration).output(output_file).run()
        except Exception as e:
            print(f'Error trimming: {str(e)}')

        os.remove(video)  # Remove original video after trimming
        return output_file
