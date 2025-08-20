# Complete Playwright script with try/except error handling and debug prints

try:
    from playwright.sync_api import sync_playwright

    print("Script started")

    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=False)  # Browser visible for debugging
        print("Creating new page...")
        page = browser.new_page()
        product_url = "https://www.croma.com/vivo-y29-5g-6gb-ram-128gb-glacier-blue-/p/312576"
        print(f"Navigating to: {product_url}")
        page.goto(product_url)
        print("Getting page title...")
        print("Title:", page.title())
        print("Closing browser...")
        browser.close()

    print("Script finished successfully.")

except Exception as e:
    print("Error occurred:", e)
