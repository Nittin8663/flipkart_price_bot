from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # optional, comment karo debug ke liye

service = Service('/usr/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011"
driver.get(url)

time.sleep(5)  # give page some time to load JS

try:
    price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.amount[data-testid='new-price']"))
    )
    print("Price:", price_element.text)
except:
    print("Price not found")

driver.quit()
