from django.conf import settings
from .misc import Misc
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix.request import get
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
from dotenv import load_dotenv
from main.utilities.getproxy import test_proxy

load_dotenv()

# https://github.com/JuanBindez/pytubefix/issues/226 for generating token easily
# https://www.npmjs.com/package/youtube-po-token-generator npm package for automating youtube po-token


class Video:
    def __init__(self, url):
        self.url = url
        self.output_path = os.path.join(settings.MEDIA_ROOT, "downloads/")

    def youtubeLib(self):
        # Define your custom headers
        custom_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.5",
        }

        # Patch the request.get method
        def custom_get(url, extra_headers=None, timeout=None):
            if extra_headers is None:
                extra_headers = {}
            extra_headers.update(custom_headers)
            return get(self.url, extra_headers=extra_headers, timeout=timeout)

        # Apply the patch
        from pytube import request
        request.get = custom_get

        proxy = test_proxy(self.url)
        # proxy = "198.23.239.134"
        
        if proxy:
            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}",
            }
        return YouTube( 
            self.url,
            on_progress_callback=on_progress,
            use_po_token=True,
            token_file=os.path.join(settings.MEDIA_ROOT, "file.json"),
            proxies=proxies
            
            # token_file=os.path.join(settings.MEDIA_ROOT, "file.json")
        )

    def getTitle(self):
        try:
            yt = self.youtubeLib()
            video_info = [yt.title, yt.author, yt.thumbnail_url.replace('default.jpg', 'hqdefault.jpg')]
            return video_info
                
        except Exception as e:
            print(str(e))
            return "Not working"
        
    def download(self):
        # output_path = os.path.join(settings.MEDIA_ROOT, "downloads/")
        misc = Misc()
        # video_title = self.getTitle()[0]
        video_title = "Testing download"
        custom_name = misc.sanitize_filename( video_title )

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
        misc = Misc()
        video_title = 'hello'
        # video_title = self.getTitle()[0]
        custom_name = misc.sanitize_filename( video_title )

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