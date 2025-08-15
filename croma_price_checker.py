from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_croma_price(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    try:
        # Explicit wait up to 15 seconds for price element
        wait = WebDriverWait(driver, 15)
        try:
            # Try using ID first
            price_element = wait.until(EC.presence_of_element_located((By.ID, "pdp-product-price")))
        except:
            # Fallback: use data-testid
            price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-testid="new-price"]')))
        
        price_text = price_element.text
        # Remove commas, ₹, whitespace
        price_text = price_text.replace("₹", "").replace(",", "").strip()
        driver.quit()
        return int(float(price_text))  # convert to integer
    except Exception as e:
        print("Error fetching price:", e)
        driver.quit()
        return None

# Example usage
url = "https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011"
price = get_croma_price(url)
if price:
    print(f"Current price: ₹{price}")
else:
    print("Price not found.")
