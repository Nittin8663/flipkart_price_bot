import requests

url = "https://api.croma.com/offer/allchannels/v2/detail"
headers = {
    "accept": "application/json, text/plain, */*",
    "client_id": "CROMA-WEB-APP",
    "content-type": "application/json",
    "origin": "https://www.croma.com",
    "referer": "https://www.croma.com/",
    "user-agent": "Mozilla/5.0"
}
payload = {
    "skuId": "312576",
    "channel": "EC",
    "storeId": "",
    "pincode": ""
}
r = requests.post(url, headers=headers, json=payload)
print(r.status_code)
print(r.text)
