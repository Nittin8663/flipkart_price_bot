from playwright.sync_api import sync_playwright

PRODUCT_URL = "https://www.croma.com/vivo-v30-5g-12gb-ram-256gb-rom-peacock-green/p/312576"
OFFER_API_ENDPOINT = "/offer/allchannels/v2/detail"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    def handle_response(response):
        if OFFER_API_ENDPOINT in response.url:
            print(f"XHR URL: {response.url}")
            try:
                print("XHR response:", response.json())
            except Exception:
                print("Non-JSON response:", response.text())

    page.on("response", handle_response)

    page.goto(PRODUCT_URL)
    page.wait_for_timeout(8000)  # Wait for XHRs

    browser.close()
