import ffmpeg
from django.conf import settings
import os
import datetime

filename1 = os.path.join(settings.MEDIA_ROOT, "downloads/Cliffe Knechtle：  is the Old Testament God Different From the New Testament God #shorts.mp4")
output_file = os.path.join(settings.MEDIA_ROOT, "downloads/test.mp4")

def getMinuteDiff(file): 
    unixTime = os.path.getmtime(file) #get timestamp for last time file was modified
    utcTimezone = datetime.timezone.utc 
    convertedTime = datetime.datetime.fromtimestamp(unixTime, tz=utcTimezone)
    currentTime = datetime.datetime.now(datetime.timezone.utc) #return present time
    timeDiff = currentTime - convertedTime #return difference btwn currenttime and file modified time
    minuteDiff = timeDiff.total_seconds()/60 #return difference in minutes
    return minuteDiff

def deleteFiles(file, minutes=36737):
    minuteDiff = getMinuteDiff(file)
    
    if(minuteDiff >= minutes):
        os.remove(file)
        print(f'{file} successfully deleted')
    else:
        print(f'{file} can''t be deleted')
    
    
output_path = os.path.join(settings.MEDIA_ROOT, "downloads/")
files = os.listdir(output_path)
for file in files:
    print (f'{os.path.join(output_path, file)}')