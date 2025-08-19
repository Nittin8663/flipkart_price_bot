from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json

# Install selenium-wire: pip install selenium-wire
from seleniumwire import webdriver as wire_webdriver

def get_offer_from_tatadigital(product_url, sku_id):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Remove for visible browser
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")

    # Use selenium-wire to intercept requests
    driver = wire_webdriver.Chrome(options=chrome_options)

    driver.get(product_url)
    time.sleep(6)  # wait for full page load & offers to appear (adjust if needed)

    offers = []
    # Loop through all network requests
    for request in driver.requests:
        if (
            request.response
            and "benefit-offers" in request.url
            and f"skuId={sku_id}" in request.url
        ):
            try:
                data = request.response.body.decode("utf-8")
                json_data = json.loads(data)
                # Parse your offer/discount info here
                best_benefit = json_data.get("data", {}).get("bestBenefitValue", {})
                for benefit_type in ["exchangeBenefit", "nonExchangeBenefit"]:
                    benefit = best_benefit.get(benefit_type, {})
                    for offer in benefit.get("productTransactionOffers", []):
                        offers.append({
                            "section": benefit_type,
                            "title": offer.get("offerTitle"),
                            "description": offer.get("offerDescription"),
                            "savings": offer.get("promotionSavings"),
                            "type": offer.get("offerType"),
                            "promotionId": offer.get("promotionId")
                        })
                break  # Stop after first match for this SKU
            except Exception as e:
                print("Error parsing offer response:", e)
    driver.quit()
    return offers

# Example usage
product_url = "https://www.tataneu.com/croma-electronics/product/312576"  # Replace with actual product URL
sku_id = "312576"
offers = get_offer_from_tatadigital(product_url, sku_id)
for offer in offers:
    print(json.dumps(offer, indent=2))
