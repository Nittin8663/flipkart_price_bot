# croma_price_checker.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_croma_price(url):
    # Chrome options
    options = Options()
    options.add_argument("--headless=new")  # latest headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # ChromeDriver setup
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        
        # Wait for price element to be visible
        price_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span.amount[data-testid='new-price']"))
        )
        
        price = price_element.text.strip()
        return price
    
    except Exception as e:
        print("Error fetching price:", e)
        return None
    
    finally:
        driver.quit()


if __name__ == "__main__":
    product_url = "https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011"
    price = get_croma_price(product_url)
    if price:
        print(f"Price for product: {price}")
    else:
        print("Price not found.")
