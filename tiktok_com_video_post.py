"""
Project : TikTok video post
Author : Ajeet
Date : April 30, 2025

Description:
This script automates the process of uploading a video to TikTok using Selenium.
It loads a set of saved cookies to bypass the login, navigates to the upload section,
selects a video from the local system, and posts it.
"""

import json
from time import sleep
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC


def upload_video_to_tiktok(video_path: str, cookie_file: str = 'tiktok_cookies.json') -> None:
    """
    Uploads a video to TikTok using Selenium automation.

    Args:
        video_path (str): Full path to the video file to upload.
        cookie_file (str): Path to the JSON file containing TikTok session cookies.
    """
    # ===== SETUP CHROME OPTIONS =====
    options = ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Initialize driver and wait
    driver = Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    url = "https://www.tiktok.com/"

    try:
        # Step 1: Open TikTok
        driver.get(url)

        # Step 2: Load cookies
        with open(cookie_file) as f:
            cookies = json.load(f)

        for cookie in cookies:
            driver.add_cookie({
                "domain": cookie['domain'],
                "value": cookie['value'],
                "id": cookie['id'],
                "name": cookie['name']
            })

        # Step 3: Reload with authenticated session
        sleep(2)
        driver.get(url)

        # Step 4: Click Upload button
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Upload"]'))).click()

        # Step 5: Upload the video file
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))).send_keys(video_path)

        # Step 6: Click Post (enabled) button
        wait.until(EC.presence_of_element_located((
            By.XPATH, '//button[(@data-e2e="post_video_button") and (@aria-disabled="false")]'
        ))).click()

        print("Video upload initiated successfully.")
        sleep(5)

    except Exception as e:
        print(f"An error occurred during upload: {e}")
    finally:
        driver.quit()


# Example usage
if __name__ == "__main__":
    upload_video_to_tiktok("D:\\IMG_4070.mp4")

"""
reference:

"""