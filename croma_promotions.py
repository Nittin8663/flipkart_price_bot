import json

response_data = {
    "path": "/v1/product/benefit-offers",
    "timestamp": "2025-08-19T19:56:11.103Z",
    "data": {
        "bestBenefitValue": {
            "exchangeBenefit": {
                "bankOffers": [],
                "productTransactionOffers": [
                    {
                        "promotionId": "01eae2ec-0576-1000-bbea-86e16dcb4b79:CROMA90676",
                        "offerType": "MULTIBUYGROUP",
                        "offerTitle": "Tata Neu Offer - Get Rs.1450 off (applicable only on Tataneu App)",
                        "offerDescription": "Tata Neu Offer - Get Rs.1450 off (applicable only on Tataneu App)",
                        "expiry": "",
                        "promotionSavings": 1450.0,
                        "termsAndConditions": []
                    }
                ],
                "couponOffers": []
            },
            "nonExchangeBenefit": {
                "bankOffers": [],
                "productTransactionOffers": [
                    {
                        "promotionId": "01eae2ec-0576-1000-bbea-86e16dcb4b79:CROMA90676",
                        "offerType": "MULTIBUYGROUP",
                        "offerTitle": "Tata Neu Offer - Get Rs.1450 off (applicable only on Tataneu App)",
                        "offerDescription": "Tata Neu Offer - Get Rs.1450 off (applicable only on Tataneu App)",
                        "expiry": "",
                        "promotionSavings": 1450.0,
                        "termsAndConditions": []
                    }
                ],
                "couponOffers": []
            }
        }
    }
}

def extract_promotions(data):
    benefits = data.get('data', {}).get('bestBenefitValue', {})
    results = []

    for section in ['exchangeBenefit', 'nonExchangeBenefit']:
        benefit = benefits.get(section, {})
        for offer in benefit.get('productTransactionOffers', []):
            results.append({
                "section": section,
                "title": offer.get("offerTitle"),
                "description": offer.get("offerDescription"),
                "savings": offer.get("promotionSavings"),
                "type": offer.get("offerType"),
                "promotionId": offer.get("promotionId")
            })
    return results

promotions = extract_promotions(response_data)

for promo in promotions:
    print(f"Section: {promo['section']}")
    print(f"Title: {promo['title']}")
    print(f"Description: {promo['description']}")
    print(f"Savings: Rs.{promo['savings']}")
    print(f"Type: {promo['type']}")
    print(f"Promotion ID: {promo['promotionId']}")
    print("-" * 40)
