import os
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, quote
import re
from pathlib import Path

def get_file_extension(file):
# Get the file name and extension
    name, extension = os.path.splitext(file)
    return extension

def get_file_name_no_extension(file):
    return Path(file).stem

def sanitize_string(fname):
    fname = re.sub(r'[^\w\s-]', '', fname) #remove all characters except alphanumerals
    fname = re.sub(r'[-\s]+', '-', fname)  # Convert runs of spaces/hyphens to single hyphen
    return sanitize_filename(fname)

def make_url_safe(url):
    # Split the base and unsafe part
    base_url, path = url.rsplit("/", 1)
    # Safely encode the path
    safe_path = quote(path)
    # Reassemble the full safe URL
    return urljoin(base_url + "/", safe_path)


""" 
import os

def checkDirectory(filename, dir):
    if not os.path.exists(dir):
        filename = filename
    if os.path.exists(dir):
        files = os.listdir(dir)
    if not files:
        filename = filename
    else:
        for file in files:
            if file == filename:
                i = 1
                filename = f'{filename}{i}'

"""