import requests

url = "https://api.tatadigital.com/getApplicablePromotion/getApplicationPromotionsForItemOffer"

headers = {
    "authorization": "8Tksadcs85ad4vsasfasgf4sJHvfs4NiKNKLHKLH582546f646",  # tumne diya hua token
    "client_id": "CROMA",
    "origin": "https://www.croma.com",
    "referer": "https://www.croma.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "content-type": "application/x-www-form-urlencoded"
}

payload = {
    "itemId": "315011",   # Example Vivo Y19 product ka Croma ID
    "channel": "WEB",
    "storeCode": "S001"
}

response = requests.post(url, headers=headers, data=payload)

print("Status Code:", response.status_code)
try:
    print("Response JSON:", response.json())
except:
    print("Response Text:", response.text)
