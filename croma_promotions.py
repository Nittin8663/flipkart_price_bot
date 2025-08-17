from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tempfile

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")

# headless detect hone se bacho
options.add_argument("--disable-blink-features=AutomationControlled")

# real browser jaisa UA set karo
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/127.0.0.0 Safari/537.36")

# har run pe fresh Chrome profile
import tempfile
options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

driver = webdriver.Chrome(options=options)

driver.get("https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011")

print(driver.title)
driver.quit()
