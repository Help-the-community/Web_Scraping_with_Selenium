"""
The script fetches/gets the FAA airport diagram URL for the given airport code.

Author: Ajeet
Date: 03/08/2025
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import webbrowser


def GetFAAapdURL_Headless(apd_code: str) -> str | None:
    """
    Return the FAA airport diagram URL for the given airport code (e.g., 'ATL').
    Runs Chrome in headless mode with a realistic User-Agent and waits for results.
    """
    options = Options()
    options.add_argument("--headless=new")  # modern headless
    options.add_argument("--window-size=1920,1080")

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://www.faa.gov/airports/runway_safety/diagrams/")

        # Wait for search box, submit query
        ident = wait.until(EC.element_to_be_clickable((By.ID, "ident")))
        ident.clear()
        ident.send_keys(apd_code)
        ident.send_keys(Keys.RETURN)

        # Wait for results table to appear (first result table on page)
        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))

        # Find first link that points to aeronav.faa
        for a in table.find_elements(By.CSS_SELECTOR, "a[href]"):
            href = a.get_attribute("href")
            if href and "aeronav.faa" in href:
                return href

        return None  # no matching link found

    finally:
        driver.quit()


if __name__ == "__main__":
    url = GetFAAapdURL_Headless("ATL")
    webbrowser.open(url)


"""
reference:
https://stackoverflow.com/
"""