import requests

url = "https://api.tatadigital.com/getApplicablePromotion/getApplicationPromotionsForItemOffer"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "8Tksadcs85ad4vsasfasgf4sJHvfs4NiKNKLHKLH582546f646",
    "client_id": "CROMA",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.croma.com",
    "priority": "u=1, i",
    "referer": "https://www.croma.com/",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
}

data = '{"getApplicablePromotionsForItemRequest":{"itemId":"314064","programId":"01eae2ec-0576-1000-bbea-86e16dcb4b79","channelIds":["TCPCHS0003"],"status":"ACTIVE"}}'

response = requests.post(url, headers=headers, data=data)

print("Status:", response.status_code)
print("Response:", response.text)
