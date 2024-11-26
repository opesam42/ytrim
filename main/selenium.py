from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os


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

    possible_locations = [
        "/usr/bin/google-chrome-stable",  # Default location for Google Chrome
        "/opt/google/chrome/google-chrome",  # Default location in Docker setups
        "/usr/local/bin/google-chrome",     # Another common location
        "/usr/bin/chrome",                  # Another alternative
    ]
    possible_chromedriver_locations = [
        "/usr/bin/chromedriver",            # Common location for chromedriver
        "/usr/local/bin/chromedriver",      # Another common location
        "/opt/google/chrome/chromedriver",  # Often used in Docker setups
        "/usr/lib/chromium-browser/chromedriver"  # If you're using Chromium browser
    ]

    # Try to set the binary location dynamically
    for location in possible_locations:
        if os.path.exists(location):
            options.binary_location = location
            print(f"Using Chrome binary at: {location}")
            break
    else:
        print("Chrome binary not found in any of the expected locations.")
        return None  # Exit early if Chrome is not found

    # Try to find a valid chromedriver
    chromedriver_path = None
    for chromedriver_location in possible_chromedriver_locations:
        if os.path.exists(chromedriver_location):
            chromedriver_path = chromedriver_location
            print(f"Using chromedriver at: {chromedriver_path}")
            break

    if not chromedriver_path:
        print("Chromedriver not found in any of the expected locations.")
        return None  # Exit early if chromedriver is not found

    # Initialize the WebDriver with the found Chrome binary and chromedriver
    try:
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
        # Now you can use the driver as usual
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return None  # Exit early if WebDriver fails to initialize

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
        print(f"Selenium failed to connect: {str(e)}")

    finally:
        print("Closing the browser...")
        if 'driver' in locals():  # Only quit if driver was initialized
            driver.quit()  # Close the browser once done
