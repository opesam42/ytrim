import os
from pathvalidate import sanitize_filename

class Misc:
    def get_file_extension(self,file):
    # Get the file name and extension
        name, extension = os.path.splitext(file)
        return extension
    
    def sanitize_filename(self, fname):
        return sanitize_filename(fname)
