# pip install undetected-chromedriver

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

try:
    print("Launching undetected Chrome browser...")
    options = uc.ChromeOptions()
    # options.add_argument("--headless")  # Agar visible browser nahi chahiye toh ye enable karo
    options.add_argument("--window-size=1280,800")
    # Optional: User-Agent spoofing
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    driver = uc.Chrome(options=options)
    driver.implicitly_wait(10)

    product_url = "https://www.croma.com/vivo-y29-5g-6gb-ram-128gb-glacier-blue-/p/312576"
    print(f"Navigating to: {product_url}")
    driver.get(product_url)

    print("Getting page title...")
    print("Title:", driver.title)
    
    # Agar aapko page ka content ya price nikalna hai toh yahan likho:
    # Example: Price extract (change selector as per site HTML)
    try:
        price_elem = driver.find_element(By.XPATH, "//span[contains(@class,'amount')]")
        print("Price:", price_elem.text)
    except Exception as ex:
        print("Price not found:", ex)
    
    print("Closing browser...")
    driver.quit()

    print("Script finished successfully.")

except Exception as e:
    print("Error occurred:", e)
