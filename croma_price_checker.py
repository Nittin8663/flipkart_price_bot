from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ----------------- CONFIG -----------------
URL = "https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011"
PRICE_SELECTOR = "span#pdp-product-price"  # Unique id selector

# ----------------- SETUP CHROME -----------------
options = Options()
options.add_argument("--headless")  # Headless mode (remove if you want browser visible)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# ChromeDriver ko automatically download karke use karna
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(URL)

    # Price ke liye wait karo (max 10 sec)
    price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, PRICE_SELECTOR))
    )

    price = price_element.text
    print(f"Current Price: {price}")

except Exception as e:
    print("Price not found or error:", e)

finally:
    driver.quit()
