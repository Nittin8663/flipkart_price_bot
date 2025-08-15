import requests

url = "https://api.croma.com/pricing-services/v1/price?productList=315011"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "channel": "EC",
    "origin": "https://www.croma.com",
    "priority": "u=1, i",
    "referer": "https://www.croma.com/",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
}

response = requests.get(url, headers=headers)
response.raise_for_status()

data = response.json()

# Print raw JSON to inspect
print("API Response:", data)

# Try to extract price if available
if data and "price" in str(data).lower():
    # You can adjust key names depending on actual JSON structure
    try:
        product_id = list(data.keys())[0]
        price_info = data[product_id]
        print("Selling Price:", price_info.get("sellingPrice", "N/A"))
        print("MRP:", price_info.get("mrp", "N/A"))
    except Exception as e:
        print("Could not parse price:", e)
else:
    print("Price data not found in API response.")
