import requests

product_id = "312576"  # Apna product id daalein

url = f"https://api.croma.com/pricing-services/v1/price?productList={product_id}"
headers = {
    "accept": "application/json, text/plain, */*",
    "origin": "https://www.croma.com",
    "referer": "https://www.croma.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}

r = requests.get(url, headers=headers)
print("Status:", r.status_code)
print("Response:", r.json())
