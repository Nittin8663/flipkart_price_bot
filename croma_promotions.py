import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

options = uc.ChromeOptions()
# options.add_argument("--headless")  # Headless off for less detection
options.add_argument("--window-size=1280,800")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

driver = uc.Chrome(options=options)
driver.get("https://www.croma.com/vivo-y29-5g-6gb-ram-128gb-glacier-blue-/p/312576")

# Simulate human actions
actions = ActionChains(driver)
actions.move_by_offset(100, 100).perform()
time.sleep(2)
driver.execute_script("window.scrollTo(0, 200);")
time.sleep(2)

print("Title:", driver.title)
# Find price or other elements as needed
try:
    price_elem = driver.find_element(By.XPATH, "//span[contains(@class,'amount')]")
    print("Price:", price_elem.text)
except Exception as ex:
    print("Price not found:", ex)

driver.quit()
