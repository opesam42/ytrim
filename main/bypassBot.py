from fake_useragent import UserAgent
import requests

def fetchPageWithHeaders(url):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Connection failed: Status code: {response.status_code}")
        return None