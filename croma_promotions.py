from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tempfile

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--disable-blink-features=AutomationControlled")

# fresh temp profile har run ke liye
profile_dir = tempfile.mkdtemp()
options.add_argument(f"--user-data-dir={profile_dir}")

# ek normal user agent
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/127.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)
driver.get("https://www.croma.com/")
print(driver.title)
driver.quit()
