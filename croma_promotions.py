from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import tempfile

def fetch_croma():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")

    # unique temp profile dir
    temp_profile = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_profile}")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011")

    print(driver.title)
    driver.quit()

if __name__ == "__main__":
    fetch_croma()
