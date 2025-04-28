"""
Project : 
Author : Ajeet
Date : Apr 27, 2025
"""
import time
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = Chrome(options=chrome_options)

driver.get("https://www.autotrader.co.uk")
wait = WebDriverWait(driver, 10)

# wait for the target iframe to get loaded in order to switch to it
wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe[id^="sp_message_iframe_"]')))

# click to 'Reject All'
wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Reject All"]'))).click()

# Switch back to the main page content
driver.switch_to.default_content()

# Now you can continue interacting with the main page here

time.sleep(5)

"""
reference:
https://stackoverflow.com/a/79593560/11179336
"""