from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_croma_price(url):
    driver.get(url)
    wait = WebDriverWait(driver, 20)  # 20 sec max wait

    # Scroll slowly to make sure dynamic content loads
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(2)

    # Try multiple possible selectors
    selectors = [
        "span.amount[data-testid='new-price']",
        "span.amount",
        "span.price",
        ".product-price .amount"
    ]

    for sel in selectors:
        try:
            price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
            price = price_element.text.strip()
            if price:
                return price
        except:
            continue

    return None

url = "https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011"
price = get_croma_price(url)
if price:
    print("Price:", price)
else:
    print("Price not found")

driver.quit()
