import pafy

url = 'https://www.youtube.com/watch?v=dyHp0TovnUQ'
video = pafy.new(url)

# print title 
print(video.title) 