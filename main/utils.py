from django.http import JsonResponse
from django.conf import settings
import os
from pytubefix import YouTube
from pytubefix.cli import on_progress
from moviepy.video.io.VideoFileClip import VideoFileClip
from .misc import Misc
import requests
from dotenv import load_dotenv

load_dotenv()

# Custom exceptions for better error handling
class VideoNotFoundError(Exception):
    """Custom exception for when the video is not found."""
    pass

class VideoDownloadError(Exception):
    """Custom exception for download errors."""
    pass

class VideoTrimError(Exception):
    """Custom exception for trimming errors."""
    pass


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
            # Fetch video metadata
            raw_page_data = fetchPageWithHeaders(self.url)
            if raw_page_data:
                yt = YouTube(self.url, on_progress_callback=on_progress, use_po_token=True,
                             token_file=os.path.join(settings.MEDIA_ROOT, "file.json"))
                video_title = yt.title
                return video_title
            else:
                raise VideoNotFoundError("Page not found or video not available.")
        except VideoNotFoundError as e:
            return JsonResponse({'error': str(e)}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Error fetching title: {str(e)}'}, status=500)

    def download(self):
        misc = Misc()
        custom_name = misc.sanitize_filename(self.getTitle())

        try:
            # Fetch video metadata
            raw_page_data = fetchPageWithHeaders(self.url)
            if raw_page_data:
                yt = YouTube(self.url, on_progress_callback=on_progress, use_po_token=True,
                             token_file=os.path.join(settings.MEDIA_ROOT, "file.json"))
                stream = yt.streams.get_highest_resolution()
                video_file = stream.download(output_path=self.output_path)
                return video_file
            else:
                raise VideoDownloadError("Failed to fetch video page.")
        except VideoDownloadError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error during video download: {str(e)}'}, status=500)

    def trim(self, start, end):
        video = self.download()  # Download the video first
        if isinstance(video, JsonResponse):
            return video  # Return early if there was a download error

        misc = Misc()
        custom_name = misc.sanitize_filename(self.getTitle())

        if not os.path.exists(video):
            raise VideoNotFoundError(f"Video file not found at path: {video}")

        extension = misc.get_file_extension(video)
        output_file = os.path.join(settings.MEDIA_ROOT, "downloads/", custom_name + '_trimmed' + extension)

        try:
            with VideoFileClip(video) as clip:
                clip = clip.with_subclip(start, end)
                clip.write_videofile(
                    output_file,
                    codec="libx264",
                    audio_codec='aac'
                )
        except VideoTrimError as e:
            return JsonResponse({'error': f'Trimming error: {str(e)}'}, status=500)
        except Exception as e:
            return JsonResponse({'error': f'Error trimming video: {str(e)}'}, status=500)

        os.remove(video)  # delete original video after trimming
        return output_file


# Example Django view to handle video operations
def video_view(request):
    try:
        video_url = request.GET.get('url')
        video = Video(video_url)
        trimmed_video = video.trim(start=0, end=30)
        if isinstance(trimmed_video, JsonResponse):
            return trimmed_video  # Return error response if trimming failed
        return JsonResponse({'message': 'Video trimmed successfully', 'video': trimmed_video})
    except VideoNotFoundError as e:
        return JsonResponse({'error': str(e)}, status=404)
    except VideoDownloadError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except VideoTrimError as e:
        return JsonResponse({'error': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)

