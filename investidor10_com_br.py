import time
from typing import List
import logging
import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ---------------------- Pandas display options ---------------------- #
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Global list to store all extracted table rows
row_list: List[List[str]] = []  # Store extracted rows


def init_driver() -> tuple[Chrome, WebDriverWait]:
    """
    Initializes Chrome driver with options and returns driver + WebDriverWait.
    """
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    return driver, wait


def processing(tbl: WebElement) -> None:
    """
    Extracts all rows from the visible table.

    Args:
        tbl: Selenium WebElement representing the table container.

    Returns:
        List of rows, each row is a list of cell strings.
    """
    table_rows = tbl.find_elements(By.CSS_SELECTOR, "div.dataTables_scrollBody>table>tbody>tr")
    for row in table_rows:
        row_list.append([d.text for d in row.find_elements(By.TAG_NAME, 'td')])


def scrape_dividends(url: str) -> pd.DataFrame:
    """
    Scrapes the dividend table from the given URL with pagination.

    Args:
        url: str - target page URL

    Returns:
        pd.DataFrame: Scraped table
    """
    driver, wait = init_driver()
    driver.get(url)

    # Wait for the dividends section to load
    wait.until(EC.visibility_of_element_located((By.ID, "dividends-section")))

    # Locate the table container
    dividend_table_container = driver.find_element(By.ID, "table-dividends-history_wrapper")

    # Scroll to the table
    driver.execute_script("arguments[0].scrollIntoView(true);", dividend_table_container)
    table = dividend_table_container.find_element(By.CSS_SELECTOR, "div.dataTables_scroll")

    # Extract table headers
    table_header_list = table.find_element(By.CSS_SELECTOR, "div.dataTables_scrollHead").text.split('\n')

    logging.info(f"Table Header: {table_header_list}")
    logging.info("Extracting Page 1...")

    # Pagination
    page_num = 2
    is_next_page = True

    # Extract first page
    processing(table)

    while is_next_page:
        try:
            next_page = dividend_table_container.find_element(
                By.CSS_SELECTOR, '#table-dividends-history_paginate>a[class="paginate_button next"]'
            )
            try:
                next_page.click()
                time.sleep(1)
                logging.info(f"Extracting Page {page_num}...")
                processing(table)
                page_num += 1
            except ElementClickInterceptedException:
                pass
        except NoSuchElementException:
            logging.info("Reached End Page")
            is_next_page = False

    df = pd.DataFrame(row_list, columns=table_header_list)
    return df


if __name__ == "__main__":
    url = "https://investidor10.com.br/acoes/vale3/"
    df = scrape_dividends(url)
    print(df)

"""
stackoverflow reference:
problem: https://stackoverflow.com/q/79735244/11179336
solution: https://stackoverflow.com/a/79735502/11179336
"""