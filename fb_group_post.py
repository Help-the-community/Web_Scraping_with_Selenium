import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver


def login() -> WebDriver:
    """
    Launch Chrome, inject cookies for facebook.com, and return the driver.

    The function:
    1) Configures common Chrome automation flags.
    2) Opens https://www.facebook.com/ to set the correct cookie scope.
    3) Loads cookies from `fb_cookies.json` and adds them to the browser.
    4) Refreshes the page to apply the authenticated session.

    Returns
    -------
    WebDriver
        An active Selenium Chrome driver, expected to be authenticated if
        the cookies are valid.

    Raises
    ------
    FileNotFoundError
        If `fb_cookies.json` does not exist.
    json.JSONDecodeError
        If the cookie file is not valid JSON.
    selenium.common.exceptions.WebDriverException
        For driver-related issues (e.g., Chrome/driver mismatch).
    """

    # Configure Chrome to start cleanly and suppress automation banners
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extension")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Create Chrome driver instance with the options above
    driver = webdriver.Chrome(options=options)

    # Open Facebook so subsequent cookie injection uses the correct domain
    driver.get("https://www.facebook.com/")

    # Open and parse the JSON cookies file
    with open("fb_cookies.json", "r", encoding="utf-8") as f:
        cookies = json.load(f)

    # Load cookies into the current domain context
    for cookie in cookies:
        driver.add_cookie(cookie)

    time.sleep(1)

    # Refresh to apply the authenticated session
    driver.refresh()

    return driver


def post_to_group(browser: WebDriver, g_name: str) -> None:
    """
    Open the Groups feed, search for a group, and click the first result.

    Parameters
    ----------
    browser : WebDriver
        An authenticated Selenium WebDriver pointing to Facebook.
    g_name : str
        The group name (or query) to search for.

    Notes
    -----
    - The XPath for the search input matches placeholders containing either
      "group" (EN) or "груп" (observed in other locales). Adjust if your UI differs.
    - After opening the first matching group, this function waits 5 seconds and exits.
      Extend this function to write a post or perform additional interactions.
    """

    # Helper for explicit waits (up to 10 seconds for each condition)
    wait = WebDriverWait(browser, 10)

    # Navigate to the Groups feed page
    browser.get("https://www.facebook.com/groups/feed/")

    # Locate and wait for the search input for groups
    group_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//input[contains(@placeholder, "груп") or contains(@placeholder, "group")]')
    ))

    # Clear any pre-filled text and submit the group name
    group_input.clear()
    group_input.send_keys(g_name)
    group_input.send_keys(Keys.ENTER)

    # Wait until the first search result container is visible
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'div[aria-label="Search results"]>div>div>div>div>div>div:nth-child(1)')
    ))

    # Wait for and click the first group's profile-photo link
    first_group = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'a[aria-label^="Profile photo of"]')
    ))
    first_group.click()

    # Keep the page visible for a short time so that you can see the desired group page opened
    time.sleep(5)

    # proceed with codes to write the post
    # .....


if __name__ == '__main__':
    # Example usage: log in and open the first "Computer Vision" group
    d = login()
    post_to_group(d, "Computer Vision")






