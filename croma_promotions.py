from seleniumwire import webdriver
import json
import time

# Product page
URL = "https://www.croma.com/apple-macbook-air-13-6-inch-m4-16gb-256gb-macos-sky-blue-/p/314064"

# Start Selenium browser
options = webdriver.ChromeOptions()
options.add_argument("--headless")   # remove this if you want to see the browser
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(seleniumwire_options={}, options=options)

try:
    print("Opening product page...")
    driver.get(URL)

    # wait for network calls to complete
    time.sleep(8)

    # check network requests
    for request in driver.requests:
        if request.response and "getApplicationPromotionsForItemOffer" in request.url:
            print(f"\n✅ Found Promotions API: {request.url}")
            print(f"Status: {request.response.status_code}")

            try:
                body = request.response.body.decode("utf-8")
                data = json.loads(body)
                print("\n--- Promotions JSON ---")
                print(json.dumps(data, indent=2))
            except Exception as e:
                print("⚠️ Could not parse JSON:", e)
            break
    else:
        print("❌ Promotions API call not found. Maybe increase sleep time.")

finally:
    driver.quit()
