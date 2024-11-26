from playwright.sync_api import sync_playwright

def fetchPageWithHeaders(url):
    try:
        with sync_playwright() as p:
            # Launch the browser (headless mode)
            browser = p.chromium.launch(headless=True)  # Change to .firefox or .webkit if needed
            page = browser.new_page()

            # Go to the URL and wait for the page to load
            page.goto(url, wait_until="load")  # Wait until page load is complete

            # Extract page content (HTML source) after JavaScript has rendered the content
            page_source = page.content()

            # Close the browser
            browser.close()

            return page_source
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None
