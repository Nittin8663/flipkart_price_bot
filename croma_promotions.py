from playwright.sync_api import sync_playwright

PRODUCT_URL = "https://www.croma.com/vivo-v30-5g-12gb-ram-256gb-rom-peacock-green/p/312576"
OFFER_XHR_SUBSTRING = "/getApplicablePromotion/getApplicationPromotionsForItemOffer"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        def handle_response(response):
            if OFFER_XHR_SUBSTRING in response.url:
                print(f"\n--- Found Offer API XHR ---\nXHR URL: {response.url}")
                try:
                    data = response.json()
                except Exception:
                    print("Non-JSON response:", response.text())
                    return

                offers = data.get("getApplicablePromotionsForItemResponse", {}).get("offerDetailsList", [])
                for offer in offers:
                    print("Offer Title:", offer.get("offerTitle"))
                    print("Description:", offer.get("description"))
                    print("Type:", offer.get("benefitType"))
                    print("Start:", offer.get("offerStartDate"), "End:", offer.get("expiryDate"))
                    print("-" * 50)

        page.on("response", handle_response)
        print(f"Opening: {PRODUCT_URL}")
        page.goto(PRODUCT_URL, timeout=60000)
        page.wait_for_timeout(20000)  # Wait for XHRs

        browser.close()

if __name__ == "__main__":
    main()
