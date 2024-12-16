import ffmpeg
from django.conf import settings
import os

filename1 = os.path.join(settings.MEDIA_ROOT, "downloads/Cliffe Knechtle：  is the Old Testament God Different From the New Testament God #shorts.mp4")
output_file = os.path.join(settings.MEDIA_ROOT, "downloads/test.mp4")

ffmpeg.input(filename1, ss=1, t=5).output(output_file).run()