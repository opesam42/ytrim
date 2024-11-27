from fake_useragent import UserAgent
import requests

ua = UserAgent()
headers = {'User-Agent': ua.random}
response = requests.get('https://www.youtube.com/shorts/3AEyyqFvQ2g', headers=headers)
print(response.status_code)
# print(response.text)