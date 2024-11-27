# from fake_useragent import UserAgent
# import requests

# def fetchPageWithHeaders(url):
#     ua = UserAgent()
#     headers = {'User-Agent': ua.random}
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         return response.content
#     else:
#         print(f"Connection failed: Status code: {response.status_code}")
#         return None
    

import requests
from fake_useragent import UserAgent

def fetchPageWithHeaders(url):
    ua = UserAgent()
    
    for _ in range(5):
        # Generate a random User-Agent for each request
        headers = {'User-Agent': ua.random}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print(f"Request {_+1}: Success!")
            # You can also return the content here if needed
            return response.content
        else:
            print(f"Request {_+1}: Connection failed with status code {response.status_code}")

    print("All requests failed.")
    return None
