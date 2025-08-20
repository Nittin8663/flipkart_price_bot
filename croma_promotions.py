import asyncio
from playwright.async_api import async_playwright
import json

async def fetch_offer_with_playwright(product_url, sku_id):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        offers = []

        async def handle_response(response):
            # Croma benefit-offers API URL check
            if "benefit-offers" in response.url and f"skuId={sku_id}" in response.url:
                try:
                    json_data = await response.json()
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
                except Exception as e:
                    print("Error parsing offer response:", e)

        page.on("response", handle_response)

        await page.goto(product_url, wait_until="networkidle")
        await asyncio.sleep(7)  # JS/API load ke liye wait

        await browser.close()
        return offers

if __name__ == "__main__":
    product_url = "https://www.croma.com/vivo-y29-5g-6gb-ram-128gb-glacier-blue-/p/312576"
    sku_id = "312576"
    offers = asyncio.run(fetch_offer_with_playwright(product_url, sku_id))
    for offer in offers:
        print(json.dumps(offer, indent=2))
