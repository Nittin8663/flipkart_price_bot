from selenium import webdriver
import time

def fetch_croma_promotions(product_url):
    driver = webdriver.Chrome()
    driver.get(product_url)

    time.sleep(6)  # thoda load hone do

    # Network sniff karna hoga (ya directly page JS run karke fetch)
    # Simple placeholder abhi ke liye:
    print("Page Loaded:", driver.title)

    driver.quit()

if __name__ == "__main__":
    url = "https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011"
    fetch_croma_promotions(url)
