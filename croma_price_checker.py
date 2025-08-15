from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Chrome driver setup
service = Service('/usr/bin/chromedriver')  # chromedriver ka path
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # agar GUI nahi chahiye
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011"

try:
    driver.get(url)
    # Explicit wait for price element
    price_element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "pdp-product-price"))
    )
    price = price_element.text
    print(f"Current price: {price}")
except TimeoutException:
    print("Price not found: Timeout")
finally:
    driver.quit()
