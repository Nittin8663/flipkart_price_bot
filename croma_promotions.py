import requests

url = "https://api.croma.com/offer/allchannels/v2/detail"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "accesstoken": "e55236f3-a403-4c77-912a-13c53b4a0e28",
    "client_id": "CROMA-WEB-APP",
    "content-type": "application/json",
    "csc_code": "null",
    "customerhash": "1ca343547f343c432b0c3dbb7ab2c4c9",
    "origin": "https://www.croma.com",
    "priority": "u=1, i",
    "referer": "https://www.croma.com/",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "source": "tcp-pwa",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}

payload = {
    "offerId": "01eae2ec-0576-1000-bbea-86e16dcb4b79:CROMA90746",
    "offerTitle": "Midnight Deals - Get Rs.1450 off (offer auto applied at cart)",
    "productCode": "312576"
}

response = requests.post(url, headers=headers, json=payload)
print(response.status_code)
print(response.text)
