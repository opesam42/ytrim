import os
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, quote

class Misc:
    def get_file_extension(self,file):
    # Get the file name and extension
        name, extension = os.path.splitext(file)
        return extension
    
    def sanitize_filename(self, fname):
        return sanitize_filename(fname)
    
    def make_url_safe(self, url):
        # Split the base and unsafe part
        base_url, path = url.rsplit("/", 1)
        # Safely encode the path
        safe_path = quote(path)
        # Reassemble the full safe URL
        return urljoin(base_url + "/", safe_path)
