# croma_price_checker_explicit_wait.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIG ---
URL = "https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011"
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"  # apna chromedriver path set karo

# --- SETUP CHROME ---
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# --- FETCH PRICE ---
try:
    driver.get(URL)

    wait = WebDriverWait(driver, 10)  # 10 sec explicit wait

    # Pehle id ke basis pe check karo
    try:
        price_element = wait.until(
            EC.presence_of_element_located((By.ID, "pdp-product-price"))
        )
    except:
        # agar id se nahi mila to data-testid ke basis pe
        price_element = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.amount[data-testid='new-price']")
            )
        )

    price_text = price_element.text.strip()
    print(f"Price: {price_text}")

except Exception as e:
    print("Error fetching price:", e)

finally:
    driver.quit()
