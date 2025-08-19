from selenium import webdriver
from selenium.webdriver.common.by import By
import time

PRODUCT_URL = "https://www.croma.com/vivo-v30-5g-12gb-ram-256gb-rom-peacock-green/p/312576"

driver = webdriver.Chrome()
driver.get(PRODUCT_URL)
time.sleep(5)  # Wait for the page/XHRs to load

# Find visible offer/promotion sections (adjust selector as per Croma site update)
try:
    offer_elems = driver.find_elements(By.CSS_SELECTOR, ".offers-sec, .offers-section, .offerText, .offer-details")
    if not offer_elems:
        offer_elems = driver.find_elements(By.XPATH, "//div[contains(text(),'Offer') or contains(text(),'Promotion')]")
    for elem in offer_elems:
        print(elem.text)
except Exception as e:
    print("Error extracting offers:", e)

driver.quit()
