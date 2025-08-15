from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Chrome options (headless mode)
options = Options()
options.add_argument("--headless")  # background me run kare
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

# Driver setup
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Check price function
def get_croma_price(url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Cookies popup handle karna
        try:
            accept_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"))
            )
            accept_btn.click()
            print("Cookies popup closed")
        except:
            pass

        # Scroll karke JS load karna
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # thoda wait for lazy load

        # Price locate karna
        price_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.amount[data-testid='new-price']"))
        )
        price = price_element.text.strip()
        return price

    except Exception as e:
        print("Error fetching price:", e)
        return None

# Example URL
url = "https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011"
price = get_croma_price(url)
if price:
    print("Price:", price)
else:
    print("Price not found")

driver.quit()
