from playwright.sync_api import sync_playwright

PRODUCT_URL = "https://www.croma.com/vivo-v30-5g-12gb-ram-256gb-rom-peacock-green/p/312576"
OFFER_API_ENDPOINT = "/offer/allchannels/v2/detail"  # Only XHRs matching this substring will be printed

def main():
    with sync_playwright() as p:
        # Launch headless browser for server compatibility
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # This function will be called for every network response
        def handle_response(response):
            if OFFER_API_ENDPOINT in response.url:
                print(f"\n--- Found Offer API XHR ---\nXHR URL: {response.url}")
                try:
                    # Try to print JSON response
                    print("XHR response:", response.json())
                except Exception:
                    # If not JSON, print raw text
                    print("Non-JSON response:", response.text())

        page.on("response", handle_response)

        print(f"Opening: {PRODUCT_URL}")
        page.goto(PRODUCT_URL, timeout=60000)
        page.wait_for_timeout(10000)  # Wait for XHRs to fire (10 seconds)

        browser.close()

if __name__ == "__main__":
    main()
