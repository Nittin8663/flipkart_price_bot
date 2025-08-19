import requests

url = "https://api.tatadigital.com/getApplicablePromotion/getApplicationPromotionsForItemOffer"

payload = {
    "getApplicablePromotionsForItemRequest": {
        "itemId": "312576",  # Product ID
        "programId": "01eae2ec-0576-1000-bbea-86e16dcb4b79",
        "channelIds": ["TCPCHS0003"],
        "status": "ACTIVE",
        "customerHash": "1ca343547f343c432b0c3dbb7ab2c4c9"
    }
}

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "Bearer e55236f3-a403-4c77-912a-13c53b4a0e28",
    "client_id": "CROMA-WEB-APP",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.croma.com",
    "referer": "https://www.croma.com/",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    # Add cookies if needed, e.g.:
    # "cookie": "ak_bmsc=...; bm_sz=..."
}

# For application/x-www-form-urlencoded, send as key=value string
import json
data = f"getApplicablePromotionsForItemRequest={json.dumps(payload['getApplicablePromotionsForItemRequest'])}"

response = requests.post(url, headers=headers, data=data)
print("Status code:", response.status_code)
print("Response:")
try:
    promotions = response.json()
    for offer in promotions.get("getApplicablePromotionsForItemResponse", {}).get("offerDetailsList", []):
        print(f"Title: {offer['offerTitle']}")
        print(f"Desc: {offer['description']}")
        print(f"Type: {offer['benefitType']}")
        print(f"Start: {offer['offerStartDate']}  End: {offer['expiryDate']}")
        print("-" * 40)
except Exception as e:
    print("Failed to parse JSON:", e)
    print(response.text)
