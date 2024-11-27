from fake_useragent import UserAgent
import requests

ua = UserAgent()
headers = {'User-Agent': ua.random}
response = requests.get('https://www.youtube.com/shorts/3AEyyqFvQ2g', headers=headers)
print(response.status_code)
# print(response.text)




import time
import requests

url = "https://example.com"
headers = {"User-Agent": "Mozilla/5.0"}

for _ in range(5):
    response = requests.get(url, headers=headers)
    if response.status_code == 429:
        print("Too many requests, waiting...")
        time.sleep(10)  # Wait longer before retrying
    else:
        print(response.text)
        break
