import requests

API_URL = "https://api.tatadigital.com/api/v1/commerce/benefit-offers"
params = {
    "skuId": "312576",
    "category": "electronics",
    "pinCode": "400001",
    "categoryId": "10"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "client_id": "TCP-WEB-APP",
    "client_secret": "6fe27bd7-658d-4d28-ab66-a71da9637529",
    "content-type": "application/json",
    "origin": "https://www.tataneu.com",
    "referer": "https://www.tataneu.com/",
    "neu-app-version": "6.1.0",
    # Add any other required headers here, like cookies, session IDs, etc.
}

response = requests.get(API_URL, params=params, headers=headers)
if response.status_code == 200:
    try:
        data = response.json()
        print("Promotions Response:")
        print(data)
        # Agar aapko specific fields chahiye:
        # Example: print all offer titles
        if "offers" in data:
            for offer in data["offers"]:
                print("Offer Title:", offer.get("offerTitle"))
                print("Description:", offer.get("description"))
                print("-" * 40)
    except Exception as e:
        print("Error parsing JSON:", e)
        print("Raw response:", response.text)
else:
    print("API Error:", response.status_code, response.text)
