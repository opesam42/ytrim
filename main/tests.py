
import m3u8
url = 'https://www.youtube.com/watch?v=dyHp0TovnUQ'
playlist = m3u8.load(url)
for segment in playlist.segments:
    with open('video.mp4', 'wb') as file:
        file.write(segment.uri)