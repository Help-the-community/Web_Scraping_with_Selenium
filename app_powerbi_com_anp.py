"""
Project : PowerBI App
Author : Ajeet
Date : April 22, 2025
"""
# ===== IMPORTS =====
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


# ===== SETUP OPTIONS =====
def initialize_driver() -> webdriver.Chrome:
    """Initializes and returns a configured Chrome WebDriver."""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("force-device-scale-factor=0.95")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    return webdriver.Chrome(options=options)


driver = initialize_driver()
wait = WebDriverWait(driver, 10)


# ===== HELPER FUNCTIONS =====
def wait_and_click(by: By, identifier: str) -> None:
    """
    Waits for an element to be clickable and clicks it.

    Args:
        by (By): Locator strategy (e.g., By.XPATH, By.CSS_SELECTOR).
        identifier (str): The locator string for the target element.
    """
    element = wait.until(EC.element_to_be_clickable((by, identifier)))
    element.click()


def scroll_slicer_container(offset_y: int = 100) -> None:
    """
    Scrolls inside a slicer dropdown popup using ActionChains.

    Args:
        offset_y (int): The vertical scroll offset. Positive = down, Negative = up.
    """
    sc = driver.find_element(By.CSS_SELECTOR,
        'div[id^="slicer-dropdown-popup-"]>div>div>div:nth-child(2)>div>div:nth-child(3)'
    )
    action = ActionChains(driver)
    action.move_to_element(sc).click_and_hold().move_by_offset(0, offset_y).release().perform()


# ===== MAIN FUNCTION =====
def report_analyser(year: str, month: int) -> None:
    """
    Navigates to a Power BI report and selects a specific month in a slicer filter.

    Args:
        year (str): The target year to expand in the slicer (e.g., "2022").
        month (int): The month to select (1-based index corresponding to the slicer position).
    """
    url = "https://app.powerbi.com/view?r=eyJrIjoiZWIzNDg3YzUtMGFlMC00MzdmLTgzOWQtZThkOWExNTU2NjBlIiwidCI6IjQ0OTlmNGZmLTI0YTYtNGI0Mi1iN2VmLTEyNGFmY2FkYzkxMyJ9"
    driver.get(url)

    # Wait for page to load and navigate to second page
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Mercado Page navigation . Mercado"]')))
    wait_and_click(By.CSS_SELECTOR, '#embedWrapperID>div.logoBarWrapper>logo-bar>div>div>div>logo-bar-navigation>span>button:nth-child(3)')

    # Open the slicer dropdown
    wait_and_click(By.CSS_SELECTOR,
        '#pvExplorationHost > div > div > exploration > div > explore-canvas > div > div.canvasFlexBox > div > div.displayArea.disableAnimations.fitToPage > div.visualContainerHost.visualContainerOutOfFocus > visual-container-repeat > visual-container:nth-child(6) > transform > div > div.visualContent > div > div > visual-modern > div > div > div.slicer-content-wrapper > div>i'
    )

    # Expand the year to show months
    wait_and_click(By.XPATH, f'//div[@class="slicerItemContainer" and @title="{year}"]/div[@class="expandButton"]')
    sleep(3)

    # Scroll and select the month
    scroll_slicer_container(offset_y=100)
    sleep(2)
    wait_and_click(By.XPATH, f'//div[@class="slicerItemContainer" and @aria-posinset="{month}"]')
    sleep(2)


# ===== RUN SCRIPT =====
if __name__ == "__main__":
    report_analyser('2023', 7)

"""
reference:
https://stackoverflow.com/a/79585038/11179336
"""
