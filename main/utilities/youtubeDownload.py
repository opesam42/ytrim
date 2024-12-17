import os
from django.conf import settings
import ffmpeg
import yt_dlp
from main.utilities.getproxy import test_proxy
from .helper_func import sanitize_string, get_file_extension, get_file_name_no_extension


class Video:
    def __init__(self, url):
        self.url = url
        self.output_path = os.path.join(settings.MEDIA_ROOT, "downloads/")

    def youtubeLib(self):
        # Define your custom headers for mimicking a browser
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

        # Define the visitor data and po_token
        visitor_data = "CgtCSmxmdzlJZi15byjtkZG6BjIKCgJORxIEGgAgZw%3D%3D"  # Replace with the actual visitor_data
        po_token = "Ijg35TfmUKF_FXSCQ6ZkiE-IU59br22MBtBVnF2RXL9w03WPfq50gn2qZZ1-oHCCdoJtkhLWc8AEoQ=="  # Replace with the actual po_token

        # yt-dlp options, including custom headers, proxy, visitor data, and po_token
        ydl_opts = {
            'proxy': proxies.get("http"),  # Use proxy if available
            # 'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),  # Set download path template
            'format': 'best',  # Download best quality video
            'noplaylist': True,  # Download only the video, not the whole playlist
            'headers': custom_headers,  # Custom headers to mimic a real browser
            # 'extractor-args': 
            # f"youtube:visitor_data={visitor_data},youtube:po_token={po_token}",  # Pass visitor data and po_token
            'extractor-args': f"youtube:visitor_data={visitor_data}",
            'nocheckcertificate': True,  # Bypass SSL certificate verification
        }

        return ydl_opts

    def getTitle(self):
        try:
            ydl_opts = self.youtubeLib()
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url, download=False)
                video_info = [
                    info_dict.get('title', 'Unknown'),
                    info_dict.get('uploader', 'Unknown'),
                    info_dict.get('thumbnail', '').replace('default.jpg', 'hqdefault.jpg')
                ]
                return video_info
        except Exception as e:
            print(f"Error retrieving video title: {str(e)}")
            return "Not working"
        
    def download(self, max_retries = 5):
       
        attempts = 0 #counter for retries

        while attempts < max_retries:
            try:
                ydl_opts = self.youtubeLib()
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(self.url, download=False) #extract video, but dont download
                    sanitized_title = sanitize_string(info_dict['title']) #clean title 
                    ydl_opts['outtmpl'] = os.path.join(self.output_path, f"{sanitized_title}.%(ext)s")

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl_updated:
                        ydl_updated.download([self.url])

                    # video_file = os.path.join(self.output_path, f"{sanitized_title}.{info_dict['ext']}")
                    video_file = os.path.join(self.output_path, f"{sanitized_title}.mp4")
                    return video_file
                
            except Exception as e:
                attempts += 1
                print(f'Error during video download {attempts}/{max_retries}: {str(e)}')
                
            
        print(f'Max retries reached. Download failed')
        return None

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
