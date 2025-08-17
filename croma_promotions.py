import requests

url = "https://api.tatadigital.com/getApplicablePromotion/getApplicationPromotionsForItemOffer"

headers = {
    "accept": "application/json, text/plain, */*",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.croma.com",
    "referer": "https://www.croma.com/",
    "authorization": "8Tksadcs85ad4vsasfasgf4sJHvfs4NiKNKLHKLH582546f646",  # apna fresh token daalna
    "client_id": "CROMA",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Yeh JSON ko string bana ke bhejna hoga
payload = ' {"getApplicablePromotionsForItemRequest":{"itemId":"314064","programId":"01eae2ec-0576-1000-bbea-86e16dcb4b79","channelIds":["TCPCHS0003"],"status":"ACTIVE"}} '

response = requests.post(url, headers=headers, data=payload)

print(response.status_code)
print(response.text)
