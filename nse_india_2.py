import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

options = Options()
options.add_argument("--start-maximized")
options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Initialize WebDriver
with webdriver.Chrome(options=options) as driver:
    wait = WebDriverWait(driver, 10)
    action = ActionChains(driver)

    try:
        print("Opening NSE announcements page...")
        driver.get("https://www.nseindia.com/companies-listing/corporate-filings-announcements")

        # Select SME tab
        sme_tab = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#containTabNav > li:nth-child(2) > a"))
        )
        action.move_to_element(sme_tab).click().perform()
        time.sleep(2)

        # Select '1W' tab
        one_week_tab = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            'div[id="Announcements_sme"]>div:nth-child(2)>div>div.block-detail-dates-box>div>div>ul>li:nth-child(2)'))
        )
        action.move_to_element(one_week_tab).click().perform()
        time.sleep(2)

        # Wait for the table to load
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#CFanncsmeTable>tbody>tr>td>a')))

        # Download the CSV
        print("Downloading CSV file...")
        download = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#CFanncsme-download'))
        )
        action.move_to_element(download).click().perform()

        # Wait for the download to complete
        time.sleep(5)
        print(f"File downloaded!")

    except TimeoutException as e:
        print(f"Timeout occurred: {e}")
        print("Please try running the script again.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
