from django.conf import settings
from .helper_func import sanitize_string, get_file_extension, get_file_name_no_extension
import ffmpeg
from main.utilities.getproxy import test_proxy
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
# from requests import get
import requests
from dotenv import load_dotenv
from typing import Callable, Tuple, Optional

load_dotenv()

# https://github.com/JuanBindez/pytubefix/issues/226 for generating token easily
# https://www.npmjs.com/package/youtube-po-token-generator npm package for automating youtube po-token

po_token_verifier: Optional[Callable[[], Tuple[str, str]]] = None
def example_verifier() -> Tuple[str, str]:
    return "Ijg35TfmUKF_FXSCQ6ZkiE-IU59br22MBtBVnF2RXL9w03WPfq50gn2qZZ1-oHCCdoJtkhLWc8AEoQ==", "CgtCSmxmdzlJZi15byjtkZG6BjIKCgJORxIEGgAgZw%3D%3D"
po_token_verify = example_verifier
class Video:
    def __init__(self, url):
        self.url = url
        self.output_path = os.path.join(settings.MEDIA_ROOT, "downloads/")

    def youtubeLib(self):
        custom_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.5",
        }

        # Test the proxy
        proxy = test_proxy(self.url)
        
        # If a proxy is found, configure it
        if proxy:
            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}",
            }
        else:
            proxies = {}

        return YouTube( 
            self.url,
            on_progress_callback=on_progress,
            use_po_token=True,
            proxies=proxies,
            po_token_verifier=po_token_verify,
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
