from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://www.croma.com/vivo-v30-5g-12gb-ram-256gb-rom-peacock-green/p/312576")

time.sleep(5)  # wait for page and XHRs to load

# Get price from page (change selector as per site update)
price_elem = driver.find_element(By.CSS_SELECTOR, "span.amount")  # Check actual selector!
print("Product Price:", price_elem.text)

# For advanced use: Use BrowserMobProxy to capture XHR requests if needed
driver.quit()
