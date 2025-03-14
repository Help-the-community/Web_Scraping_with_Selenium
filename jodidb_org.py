from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains


options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

# Suppress logging to reduce unnecessary output
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Set up the WebDriver with configured options
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.maximize_window()
wait = WebDriverWait(browser, 10)


browser.get(r'http://www.jodidb.org/TableViewer/tableView.aspx?ReportId=93905')

import time
time.sleep(2)

columns = []


scroll_thumb = browser.find_element(By.CSS_SELECTOR, "#hScrollTD")  # Replace with your thumb element

action = ActionChains(browser)

for _ in range(1, 50):
    for i in range(0, 15):
        col_names = browser.find_element(By.CSS_SELECTOR, f'table[id="DataTable"]>thead>tr>#a{i}').text
        columns.append(col_names)

    sleep(2)
    action.click_and_hold(scroll_thumb).move_by_offset(20, 0).release().perform()
    sleep(1)

print(columns)