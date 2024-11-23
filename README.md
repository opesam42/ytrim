function i learned

request.POST.get() - to get the value of a form input when you are not using django inbuilt form
if request.method == 'POST':
        videoLink = request.POST.get('ylink')
        return HttpResponse(videoLink)

pytube keeps giving me this as error
Exception while accessing title of https://youtube.com/watch?v=5ipHezg75Jc. Please file a bug report at https://github.com/pytube/pytube

switch to pafy
ImportError: pafy: youtube-dl not found; you can use the internal backend by setting the environmental variable PAFY_BACKEND to "internal". It is not enabled by default because it is not as well maintained as the youtube-dl backend.
have to install youtube-dl

not working
so install YT-DLP pip install --upgrade yt-dlp

using media root

os.path.join

pip install ffmpeg-python

using moviepy

