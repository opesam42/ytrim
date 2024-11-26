import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def fetchPageWithHeaders(url):
    # Setup Chrome options to run the browser in headless mode (without UI)
    options = Options()
    options.add_argument("--headless")  # Run headless (without opening a browser window)
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("start-maximized")  # Start in maximized window (optional)
    options.add_argument("disable-infobars")  # Disable infobars like "Chrome is being controlled by automated test software"
    options.add_argument("--disable-extensions")  # Disable Chrome extensions
    options.add_argument("--no-sandbox")  # Disable sandboxing (can be required on certain systems)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0")

    # Explicitly set Chrome binary location
    # options.binary_location = "/usr/bin/chromium-browser"
    options.binary_location = "/usr/bin/google-chrome-stable"

    # Initialize WebDriver (uses the appropriate ChromeDriver version automatically)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open the URL (e.g., YouTube video URL)
        print(f"Attempting to load URL: {url}")
        driver.get(url)

        # Wait for the page to load
        time.sleep(3)  # You can adjust the sleep time based on the page load speed

        # Extract page content (HTML source) after JavaScript has rendered the content
        page_source = driver.page_source
        print("Page loaded successfully.")
        return page_source

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(f"Selenium failed to connect. Error details: {e}")

    finally:
        print("Closing the browser...")
        driver.quit()  # Close the browser once done
