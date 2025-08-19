from playwright.sync_api import sync_playwright

PRODUCT_URL = "https://www.croma.com/vivo-v30-5g-12gb-ram-256gb-rom-peacock-green/p/312576"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Print every XHR request URL for debugging
        def handle_response(response):
            if response.request.resource_type == "xhr":
                print(f"XHR: {response.url}")

        page.on("response", handle_response)

        print(f"Opening: {PRODUCT_URL}")
        page.goto(PRODUCT_URL, timeout=60000)

        # Scroll & click to trigger more offers
        page.mouse.wheel(0, 2000)
        page.wait_for_timeout(2000)
        try:
            page.click("text='View All Offers'")
        except Exception as e:
            print(f"No 'View All Offers' button: {e}")

        page.wait_for_timeout(30000)  # Wait longer for all XHRs

        browser.close()

if __name__ == "__main__":
    main()
