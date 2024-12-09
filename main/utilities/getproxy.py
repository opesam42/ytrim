import requests
from bs4 import BeautifulSoup

url = 'https://free-proxy-list.net/'

def scraper():
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure we got a valid response
        soup = BeautifulSoup(response.text, 'html.parser')

        proxies_list = []

        for row in soup.find("table", attrs={"class": "table-striped"}).find_all("tr")[1:]:
            tds = row.find_all("td")
            try:
                ip = tds[0].text.strip()      # First column: IP address
                port = tds[1].text.strip()    # Second column: Port
                https_support = tds[6].text.strip().lower()  # Seventh column: HTTPS support
                anonymity = tds[4].text.strip().lower()

                if https_support == "yes" and anonymity == "elite proxy":    # Check if HTTPS is supported
                    proxies_list.append(f"{ip}:{port}")
            except IndexError:
                continue
        print(proxies_list)
        return proxies_list

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching proxies: {e}")
        return []


# check working proxy
def test_proxy(url):
    # url = "http://httpbin.org/ip"
    # url = "http://youtube.com"
    proxies = scraper()

    for i in range(len(proxies)):

        #printing req number
        print("Request Number : " + str(i+1))
        proxy = proxies[i]

        try:
            response = requests.get(
                url,
                timeout=10,
                proxies = {"http":proxy, "https":proxy}
            )
            if response.status_code == 200:
                print(f"Found working proxy: {proxy}")
                return proxy
            
        except requests.exceptions.ConnectTimeout:
            print(f"Proxy {proxy} timed out.")
        except requests.exceptions.RequestException as e:
            print(f"Proxy {proxy} failed. Error: {e}")
            
    # if none is working
    print("No working proxy found")
    return None