import requests

url = "https://api.croma.com/pricing-services/v1/price?productList=315011"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "channel": "EC",
    "origin": "https://www.croma.com",
    "referer": "https://www.croma.com/",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # raise exception for HTTP errors
    data = response.json()
    
    # Extract price from response
    product_id = "315011"
    if "priceResponse" in data and product_id in data["priceResponse"]:
        price_info = data["priceResponse"][product_id]
        price = price_info.get("finalPrice", "Price not found")
        print(f"Product {product_id} price: ₹{price}")
    else:
        print("Price data not found in API response.")

except requests.exceptions.RequestException as e:
    print("Error fetching price:", e)
