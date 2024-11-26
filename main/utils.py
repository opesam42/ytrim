from django.conf import settings
from .misc import Misc
from .selenium import fetchPageWithHeaders
from pytubefix import YouTube
from pytubefix.cli import on_progress
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
# from requests import get
import requests
from dotenv import load_dotenv
 

load_dotenv()

import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# You can add a file handler if you want to store logs in a file
file_handler = logging.FileHandler('video_processing.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


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
            # Fetch video metadata
            raw_page_data = fetchPageWithHeaders(self.url)
            
            if raw_page_data:
                yt = YouTube(self.url, on_progress_callback=on_progress, use_po_token=True,
                             token_file=os.path.join(settings.MEDIA_ROOT, "file.json"))
                video_title = yt.title
                return video_title
            else:
                logger.error(f"Page not found for URL: {self.url}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching title for URL {self.url}: {str(e)}")
            raise ValueError(f"Failed to fetch video title for {self.url}")  # Raise a specific exception

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
                logger.error(f"Page not fetched for URL: {self.url}")
                return None
            
        except Exception as e:
            logger.error(f"Error during video download for URL {self.url}: {str(e)}")
            raise RuntimeError(f"Failed to download video for {self.url}")  # Raise a specific exception

    def trim(self, start, end):
        video = self.download()
        misc = Misc()
        custom_name = misc.sanitize_filename(self.getTitle())

        if os.path.exists(video):
            logger.info(f'{video} found')
        else:
            logger.warning(f"Video file {video} not found")
        
        extension = misc.get_file_extension(video)  # Get extension of file
        output_file = os.path.join(settings.MEDIA_ROOT, "downloads/", custom_name + '_trimmed' + extension)

        try:
            with VideoFileClip(video) as clip:
                clip = clip.with_subclip(start, end)
                clip.write_videofile(output_file, codec="libx264", audio_codec='aac')
            logger.info(f"Video trimmed and saved to {output_file}")
        except Exception as e:
            logger.error(f"Error trimming video {video}: {str(e)}")
            raise RuntimeError(f"Failed to trim video {video}")

        os.remove(video)  # Delete original video after trimming
        return output_file
