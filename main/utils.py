from django.conf import settings
from .misc import Misc
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
from dotenv import load_dotenv

load_dotenv()

class Video:
    def __init__(self, url):
        self.url = url
        self.output_path = os.path.join(settings.MEDIA_ROOT, "downloads/")

    def getTitle(self):
        try:
            ydl_opts = {}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url, download=False)
                video_title = info_dict.get('title', 'Unknown title')
                return video_title
                
        except Exception as e:
            print(str(e))
            return "Not working"
        
    def download(self):
        try:
            # output_path = os.path.join(settings.MEDIA_ROOT, "downloads/")
            misc = Misc()
            custom_name = misc.sanitize_filename( self.getTitle() )

            ydl_opts = {
                'outtmpl': f'{self.output_path}{custom_name}.%(ext)s',
                'concurrent_fragments': 16,  # Download in 16 simultaneous chunks (adjust based on connection)
                'fragment_retries': 10,  # Retry downloading fragments in case of failure
                'retry_max': 10,  # Max retries for the download

                # Using user-agent option in yt-dlp to simulate a real browser and bybass YouTubebot detection
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                'cookies-from-browser': 'chrome',
                'cookies': os.path.join(settings.MEDIA_ROOT, "ytcookies.txt"),
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url, download=True)
                video_file = ydl.prepare_filename(info_dict)
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

        
