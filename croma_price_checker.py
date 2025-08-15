# croma_price_checker.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Chrome options
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Setup Chrome driver using webdriver_manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL of the Croma product
url = "https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011"

try:
    driver.get(url)
    time.sleep(3)  # wait for page to load

    # Locate price element
    price_element = driver.find_element(By.CSS_SELECTOR, "span.amount[data-testid='new-price']")
    price = price_element.text.strip()
    print(f"Price found: {price}")

except Exception as e:
    print(f"Error fetching price: {e}")

finally:
    driver.quit()
