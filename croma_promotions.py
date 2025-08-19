import requests

url = "https://api.croma.com/offer/allchannels/v2/detail"

headers = {
    "accept": "application/json, text/plain, */*",
    "accesstoken": "e55236f3-a403-4c77-912a-13c53b4a0e28",  # apni latest value lagao!
    "client_id": "CROMA-WEB-APP",
    "customerhash": "1ca343547f343c432b0c3dbb7ab2c4c9",      # apni latest value lagao!
    "origin": "https://www.croma.com",
    "referer": "https://www.croma.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "content-type": "application/json"
}

payload = {
    "offerId": "01eae2ec-0576-1000-bbea-86e16dcb4b79:CROMA90746",
    "offerTitle": "Midnight Deals - Get Rs.1450 off (offer auto applied at cart)",
    "productCode": "312576"
}

response = requests.post(url, headers=headers, json=payload)
print(response.status_code)
print(response.text)
