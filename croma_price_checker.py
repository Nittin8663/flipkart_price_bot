from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Chrome setup
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def get_croma_price(url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        # Cookies popup close
        try:
            accept_btn = wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            accept_btn.click()
        except:
            pass

        # Scroll down to make sure price loads
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(2)

        # Try multiple selectors for price
        selectors = [
            "span.amount[data-testid='new-price']",
            "span.amount",  # backup
            "span.price"    # backup
        ]

        price = None
        for sel in selectors:
            try:
                price_element = driver.find_element(By.CSS_SELECTOR, sel)
                price = price_element.text.strip()
                if price:
                    break
            except:
                continue

        return price

    except Exception as e:
        print("Error fetching price:", e)
        return None

# Example
url = "https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011"
price = get_croma_price(url)
if price:
    print("Price:", price)
else:
    print("Price not found")

driver.quit()
