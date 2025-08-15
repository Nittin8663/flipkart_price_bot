from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

URL = "https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011"
PRICE_SELECTOR = "span#pdp-product-price"  # id selector

options = Options()
# options.add_argument("--headless")  # Headless temporarily off for debugging
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(URL)
    time.sleep(3)  # Page ko render hone ke liye extra wait

    price_element = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, PRICE_SELECTOR))
    )

    price = price_element.text.strip()
    print(f"Current Price: {price}")

except Exception as e:
    print("Price not found or error:", e)

finally:
    driver.quit()
