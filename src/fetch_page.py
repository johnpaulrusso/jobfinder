from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch_page(url):
    # Configure Chrome options for headless mode if you don’t need a visible browser window
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")  # Required for Docker
    chrome_options.add_argument("--disable-dev-shm-usage")  # Avoid resource issues
    chrome_options.add_argument("--disable-gpu")  # Avoid GPU issues in headless mode
    chrome_options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging

    # Initialize the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        print('Waiting 5 seconds for page load...')
        time.sleep(5)  # Adjust sleep time as needed or use WebDriverWait for dynamic loading
        page_source = driver.page_source
    except Exception as e:
        print(f"An error occurred when fetching the web page: {e}")
        page_source = None
    finally:
        # Close the driver after use
        driver.quit()

    return page_source