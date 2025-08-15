from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Chrome options
options = Options()
options.add_argument("--headless")  # Headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Driver setup
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Croma product URL (yahan apna product URL daalein)
url = "https://www.croma.com/product/315011"  

driver.get(url)
time.sleep(3)  # Page load ke liye wait

try:
    # Price selector
    price_element = driver.find_element(By.CSS_SELECTOR, "span.amount[data-testid='new-price']")
    price = price_element.text
    print(f"Price: {price}")
except Exception as e:
    print("Price not found or error:", e)

driver.quit()
