import requests

product_code = "314064"

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
}

# 🔹 yaha form-data jaisa raw string banana hoga
payload = (
    '{"getApplicablePromotionsForItemRequest":{'
    f'"itemId":"{product_code}",'
    '"programId":"01eae2ec-0576-1000-bbea-86e16dcb4b79",'
    '"channelIds":["TCPCHS0003"],'
    '"status":"ACTIVE"}}'
)

response = requests.post(url, headers=headers, data=payload)

print("Status Code:", response.status_code)
print("Response Text:", response.text)
