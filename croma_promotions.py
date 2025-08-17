import requests
import json

# API endpoint
url = "https://api.tatadigital.com/getApplicablePromotion/getApplicationPromotionsForItemOffer"

# Headers (yaha aap apna authorization token daalna hoga jo network tab me mila tha)
headers = {
    "accept": "application/json, text/plain, */*",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.croma.com",
    "referer": "https://www.croma.com/",
    "authorization": "8Tksadcs85ad4vsasfasgf4sJHvfs4NiKNKLHKLH582546f646",  # <-- yeh replace karna hoga
    "client_id": "CROMA",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Payload (product id change kar sakte ho)
payload = {
    "getApplicablePromotionsForItemRequest": {
        "itemId": "314064",
        "programId": "01eae2ec-0576-1000-bbea-86e16dcb4b79",
        "channelIds": ["TCPCHS0003"],
        "status": "ACTIVE"
    }
}

# POST request
response = requests.post(url, headers=headers, json=payload)

# Response handling
if response.status_code == 200:
    data = response.json()
    promotions = data.get("getApplicablePromotionsForItemResponse", {}).get("promotions", [])

    print("\n📦 Offers for Product ID:", payload["getApplicablePromotionsForItemRequest"]["itemId"])
    print("="*60)

    for promo in promotions:
        print(f"🔹 {promo.get('promotionName')}")
        print(f"   ➝ Offer: {promo.get('promotionDesc')}")
        print(f"   ➝ Type: {promo.get('promotionType')}")
        print(f"   ➝ Valid Till: {promo.get('promotionValidity')}")
        if promo.get("tcUrl"):
            print(f"   ➝ Terms: {promo['tcUrl']}")
        print("-"*60)
else:
    print("❌ Error:", response.status_code, response.text)
