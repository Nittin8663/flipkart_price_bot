import requests
import json

# 1. API URL
url = "https://api.tatadigital.com/getApplicablePromotion/getApplicationPromotionsForItemOffer"

# 2. Headers (copy these fresh from your browser DevTools if possible!)
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "Bearer e55236f3-a403-4c77-912a-13c53b4a0e28",  # <--- Use fresh token!
    "client_id": "CROMA-WEB-APP",
    "content-type": "application/json",
    "origin": "https://www.croma.com",
    "priority": "u=1, i",
    "referer": "https://www.croma.com/",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}

# 3. Payload
payload = {
    "getApplicablePromotionsForItemRequest": {
        "itemId": "312576",
        "programId": "01eae2ec-0576-1000-bbea-86e16dcb4b79",
        "channelIds": ["TCPCHS0003"],
        "status": "ACTIVE",
        "customerHash": "1ca343547f343c432b0c3dbb7ab2c4c9"
    }
}

# 4. Make API Call
response = requests.post(url, headers=headers, json=payload)
print("HTTP Status:", response.status_code)

try:
    response_json = response.json()
except Exception as e:
    print("Error parsing response JSON:", e)
    print(response.text)
    exit()

# 5. Extract ONLY the 1450 Wala Offer
def get_1450_offer(response_json):
    offers = response_json.get('getApplicablePromotionsForItemResponse', {}).get('offerDetailsList', [])
    for offer in offers:
        if offer.get("offerId") == "01eae2ec-0576-1000-bbea-86e16dcb4b79:CROMA90746":
            return offer
    return None

offer_1450 = get_1450_offer(response_json)

if offer_1450:
    print("\n--- 1450 Wala Offer ---")
    print("Offer Title:", offer_1450["offerTitle"])
    print("Description:", offer_1450["description"])
    print("Offer ID:", offer_1450["offerId"])
    print("Benefit Type:", offer_1450["benefitType"])
    print("Type:", offer_1450["offerType"])
    print("Start:", offer_1450["offerStartDate"])
    print("Expiry:", offer_1450["expiryDate"])
    print("Redemption Limit:", offer_1450.get("offerRedemptionLimit"))
    print("Redemption Left:", offer_1450.get("offerRedemptionLimitLeft", "N/A"))
    print("Blackout Periods:")
    for period in offer_1450.get("blackOutPeriod", []):
        print("  From", period["blackOutStartDate"], "to", period["blackOutEndDate"])
else:
    print("1450 wala offer nahi mila!")
