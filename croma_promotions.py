from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tempfile

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")

# fresh unique user-data-dir
temp_profile = tempfile.mkdtemp()
options.add_argument(f"--user-data-dir={temp_profile}")

# headless mode if no GUI
options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)
driver.get("https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011")

print(driver.title)
driver.quit()
