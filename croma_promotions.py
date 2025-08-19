from playwright.sync_api import sync_playwright

PRODUCT_URL = "https://www.croma.com/vivo-v30-5g-12gb-ram-256gb-rom-peacock-green/p/312576"
OFFER_API_SUBSTRING = "/offer"  # Print all XHRs containing "/offer"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        def handle_response(response):
            if OFFER_API_SUBSTRING in response.url:
                print(f"\n--- Offer XHR ---\n{response.url}")
                try:
                    print(response.json())
                except Exception:
                    print(response.text())

            # For debugging, print all XHRs:
            # print(f"XHR: {response.url}")

        page.on("response", handle_response)

        print(f"Opening: {PRODUCT_URL}")
        page.goto(PRODUCT_URL, timeout=60000)

        # Try simulating a click to trigger more offers (if any)
        try:
            page.click("text='View All Offers'")
        except Exception:
            pass

        page.wait_for_timeout(20000)  # Wait longer for all XHRs

        browser.close()

if __name__ == "__main__":
    main()
