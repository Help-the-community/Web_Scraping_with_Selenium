"""
Script to search for a stock ticker (e.g., NVDA) on Google Finance using Selenium.

Author: Ajeet
Date: 17/05/2025
"""

import time

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_driver():
    """
    Set up and return a Selenium Chrome WebDriver with custom options.
    """
    options = ChromeOptions()
    options.add_argument("--start-maximized")  # Launch browser maximized
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    return Chrome(options=options)


def search_stock(driver, stock_name: str):
    """
    Automates the stock search on Google Finance.

    Args:
        driver: Selenium WebDriver instance.
        stock_name (str): Name of the stock to search for (e.g., "nvda stock").
    """
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.google.com/finance/")

    # Wait for search input fields to load and select the second input field
    input_elements = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, 'input[aria-label="Search for stocks, ETFs & more"]')
    ))

    if len(input_elements) < 2:
        raise Exception("Expected input field not found.")

    input_element = input_elements[1]
    input_element.send_keys(stock_name)
    time.sleep(1)
    input_element.send_keys(Keys.ENTER)
    time.sleep(2)


def main():
    """
    Main function to execute the script.
    """
    driver = setup_driver()
    search_stock(driver, "nvda stock")


if __name__ == "__main__":
    main()

"""
reference:
https://stackoverflow.com/a/79626737/11179336
"""