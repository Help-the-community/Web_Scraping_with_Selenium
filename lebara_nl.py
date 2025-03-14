import time
import random
from time import sleep

import pyautogui
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# Use undetected-chromedriver
driver = uc.Chrome()
driver.maximize_window()
driver.get("https://www.lebara.nl/nl/prepaid/data-bundle-valuesim.html")

# Simulate human-like behavior
time.sleep(random.uniform(1, 3))
pyautogui.moveTo(random.randint(100, 500), random.randint(100, 500), duration=0.5)

# Click the cookie decline button
cookie_decline_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
cookie_decline_button.click()

# Simulate human-like behavior
time.sleep(random.uniform(1, 3))
pyautogui.moveTo(random.randint(100, 500), random.randint(100, 500), duration=0.5)

# Click the bestelSimkaartButton using JavaScript
bestel_simkaart_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div[3]/button")
bestel_simkaart_button.click()
time.sleep(2)

# Wait for the new page to load
time.sleep(5)
