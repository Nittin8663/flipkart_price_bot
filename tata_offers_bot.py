import requests

url = "https://api.tatadigital.com/getApplicablePromotion/getApplicationPromotionsForItemOffer"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "8Tksadcs85ad4vsasfasgf4sJHvfs4NiKNKLHKLH582546f646",
    "client_id": "CROMA",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.croma.com",
    "referer": "https://www.croma.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    # 👇 Ye tumhe apne browser se copy karna hai
    "cookie": "ak_bmsc=xxxx; bm_sv=yyyy; session=zzzz"
}

payload = {
    "getApplicablePromotionsForItemRequest": {
        "itemId": "314064",
        "programId": "01eae2ec-0576-1000-bbea-86e16dcb4b79",
        "channelIds": ["TCPCHS0003"],
        "status": "ACTIVE"
    }
}

response = requests.post(url, headers=headers, json=payload)

print("Status:", response.status_code)
print("Response JSON:", response.text)
