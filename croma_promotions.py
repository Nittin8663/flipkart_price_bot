try:
    from playwright.sync_api import sync_playwright

    print("Script started")

    with sync_playwright() as p:
        print("Launching browser in headless mode...")
        browser = p.chromium.launch(headless=True)  # Headless mode for server
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
