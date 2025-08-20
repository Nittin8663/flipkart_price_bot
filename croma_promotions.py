try:
    from playwright.sync_api import sync_playwright

    print("Script started")
    with sync_playwright() as p:
        print("Launching browser in headless mode...")
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        print("Creating new page with spoofed user-agent and headers...")
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()
        page.set_extra_http_headers({
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/"
        })
        product_url = "https://www.croma.com/vivo-y29-5g-6gb-ram-128gb-glacier-blue-/p/312576"
        print(f"Navigating to: {product_url}")
        page.goto(product_url, timeout=60000)
        print("Getting page title...")
        print("Title:", page.title())
        print("Closing browser...")
        browser.close()
    print("Script finished successfully.")
except Exception as e:
    print("Error occurred:", e)
