from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def main():
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 5)

    driver.get(f"https://www.transat.com/fr-CA?search=package")

    wait.until(EC.presence_of_element_located((By.ID, 'FROMSEARCH'))).click()
    sleep(2)
    driver.find_element(By.CSS_SELECTOR, '#YUL-FROMSEARCH > span.code').click()

    wait.until(EC.presence_of_element_located((By.ID, 'TOSEARCH'))).click()
    sleep(2)
    driver.find_element(By.CSS_SELECTOR, '#City-13-TOSEARCH > div > span.name').click()
    sleep(2)


if __name__ == "__main__":
    main()
