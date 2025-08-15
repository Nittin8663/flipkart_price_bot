# croma_simple_price_checker.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# --- CONFIG ---
URL = "https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011"
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"  # apna path set karo

# --- SETUP CHROME ---
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# --- FETCH PRICE ---
try:
    driver.get(URL)
    time.sleep(3)  # page load wait

    # Croma ke do possible selectors
    try:
        price_element = driver.find_element(By.CSS_SELECTOR, "span#pdp-product-price")
    except:
        price_element = driver.find_element(By.CSS_SELECTOR, "span.amount[data-testid='new-price']")

    price_text = price_element.text.strip()
    print(f"Price: {price_text}")

except Exception as e:
    print("Error fetching price:", e)

finally:
    driver.quit()
