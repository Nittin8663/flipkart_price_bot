import requests

url = "https://api.tatadigital.com/getApplicablePromotion/getApplicationPromotionsForItemOffer"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "8Tksadcs85ad4vsasfasgf4sJHvfs4NiKNKLHKLH582546f646",  # <-- apna valid token yaha daalo
    "client_id": "CROMA",
    "content-type": "application/json",
    "origin": "https://www.croma.com",
    "referer": "https://www.croma.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "cookie": (
        "ak_bmsc=CD9D25F25DA20D7D541AD3CF8EB1DB22~0000...;"  # <-- full cookie paste karo
        " bm_sz=0B804A842B54CBEB6D441928DA0967C3~YAAQ..."
    )
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
print("Response:", response.text)
