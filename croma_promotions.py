import requests

def fetch_benefit_offers(sku_id, category, pin_code, category_id):
    url = (
        "https://api.tatadigital.com/api/v1/commerce/benefit-offers"
        f"?skuId={sku_id}&category={category}&pinCode={pin_code}&categoryId={category_id}"
    )
    headers = {
        "accept": "application/json",
        # Add other headers if needed for successful response
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "origin": "https://www.tataneu.com",
        "referer": "https://www.tataneu.com/",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    offers = []
    best_benefit = data.get("data", {}).get("bestBenefitValue", {})

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
    return offers

# Example usage:
offers = fetch_benefit_offers(
    sku_id="312576",
    category="electronics",
    pin_code="400001",
    category_id="10"
)
for offer in offers:
    print(f"Section: {offer['section']}")
    print(f"Title: {offer['title']}")
    print(f"Description: {offer['description']}")
    print(f"Savings: {offer['savings']}")
    print(f"Type: {offer['type']}")
    print(f"Promotion ID: {offer['promotionId']}")
    print("-" * 40)
