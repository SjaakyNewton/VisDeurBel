import time
from urllib.request import urlopen

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def getScreenShot(website_url):
    # Set up headless Chrome for capturing screenshots
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")

    # Make sure you have chromedriver installed
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the webpage
    # url = "https://example.com/video-page"
    driver.get(website_url)

    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, "CybotCookiebotDialogBodyButtonDecline"))  # Using ID
        )
        cookie_button.click()
        print("Rejected cookies.")
    except:
        print("No cookie popup found or already Rejected.")

    video_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "js-stream"))
    )

    # Scroll to the video (optional)
    driver.execute_script("arguments[0].scrollIntoView();", video_element)
    # Wait for the page to load (adjust as needed)
    time.sleep(5)

    # Take a screenshot of the full page
    screenshot_path = "website_screenshot.png"
    video_element.screenshot(screenshot_path)
    print(f"Screenshot saved as {screenshot_path}")

    # Close the browser
    driver.quit()

    # Load and display the screenshot (optional)
    image = Image.open(screenshot_path)
    image.show()  # Opens the image for preview


def main():
    url = "https://visdeurbel.nl/"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    video = html.find("video")
    print(video)
    getScreenShot(url)


if __name__ == "__main__":
    main()
