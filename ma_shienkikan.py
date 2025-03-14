from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Initialize an empty list to store scraped data
data = []

# Function to configure Chrome options for stealth scraping
def get_stealth_chrome_options():
    options = Options()
    # Set headless mode (optional, uncomment to avoid loading browser UI)
    # options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

    # Suppress logging to reduce unnecessary output
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Ensure better resource handling for long scripts
    options.add_argument("--disable-gpu")
    options.add_argument("--enable-logging")
    return options


# Set up the WebDriver with configured options
service = Service(ChromeDriverManager().install())
options = get_stealth_chrome_options()
browser = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(browser, 10)

try:
    # Navigate to the target website
    browser.get("https://library.usask.ca/#gsc.tab=0")
    print("[INFO] Successfully loaded the website.")

    # Locate the search field and input query
    q_field = browser.find_element(By.ID, "primoQueryTemp")
    q_field.send_keys("artificial intelligence")
    q_field.send_keys(Keys.ENTER)
    print("[INFO] Search query submitted.")

    # Wait for the search results container to be visible
    results_container = wait.until(
        EC.presence_of_element_located((By.ID, "searchResultsContainer"))
    )
    print("[INFO] Search results container loaded.")

    # Scrape the first 10 search results
    for i in range(1, 11):
        try:
            # Locate each search result container by its XPath
            container = results_container.find_element(By.XPATH, f"//*[@id='searchResultsContainer']/div[{i}]")

            # Extract relevant information for each result
            item_data = {
                "item_number": container.find_element(By.CLASS_NAME, "list-item-count").text,
                "media_type": container.find_element(By.CSS_SELECTOR, "div.media-content-type.align-self-start").text,
                "image": container.find_element(By.CLASS_NAME, "media-thumbnail")
                .find_element(By.CSS_SELECTOR, "div:nth-child(1) > img")
                .get_attribute("src"),
                "item_title": container.find_element(By.CLASS_NAME, "item-title").text,
            }
            data.append(item_data)
            # print(f"[INFO] Scraped item {i}: {item_data}")
        except Exception as e:
            print(f"[WARNING] Error scraping item {i}: {e}")

    # Print the collected data
    print("[INFO] Scraping completed successfully.")
    print(data)

except Exception as e:
    print(f"[ERROR] An error occurred: {e}")

finally:
    # Ensure the browser is properly closed
    browser.quit()
    print("[INFO] Browser closed.")
