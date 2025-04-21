from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
import time
import json

options = ChromeOptions()
# open and maximize the screen
options.add_argument("--start-maximized")
# below 2 lines diables the info bar
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=options)

driver.get("https://stackoverflow.com")

#find and click the log in button
find_login_button = driver.find_element(By.XPATH,"//a[normalize-space()='Log in']").click()
# fill the email account, password
email = driver.find_element(By.XPATH, "//input[@id='email']")
password = driver.find_element(By.XPATH, "//input[@id='password']")
email.send_keys("your_mail_id")
password.send_keys("your_password")
time.sleep(2)

# click button login2
find_submit_button = driver.find_element(By.XPATH,"//button[@id='submit-button']").click()
time.sleep(2)
# print(driver.get_cookies())

json_object = json.dumps(driver.get_cookies())

# Writing to sample.json
with open("stackoverflow_cookies.json", "w") as outfile:
    outfile.write(json_object)
