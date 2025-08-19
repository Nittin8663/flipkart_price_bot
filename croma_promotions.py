import requests

url = "https://api.croma.com/pricing-services/v1/price?productList=312576"

headers = {
    "accept": "application/json, text/plain, */*",
    "client_id": "CROMA-WEB-APP",
    "origin": "https://www.croma.com",
    "referer": "https://www.croma.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/139.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.text)
