import requests

def fetch_price(product_id):
    url = f"https://api.croma.com/pricing-services/v1/price?productList={product_id}"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "channel": "EC",
        "origin": "https://www.croma.com",
        "referer": "https://www.croma.com/",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        if "pricelist" in data and len(data["pricelist"]) > 0:
            price_info = data["pricelist"][0]
            print(f"Product ID: {product_id}")
            print(f"MRP: ₹{price_info.get('mrp')}")
            print(f"Selling Price: ₹{price_info.get('sellingPriceValue')}")
            print(f"Discount %: {price_info.get('discountPercentage')}")
            print(f"Is COD Available: {price_info.get('isCODAvailable')}")
            print(f"Is EMI Available: {price_info.get('isEMIAvailable')}")
            print(f"Is Exchange Available: {price_info.get('isExchangeAvailable')}")
            print("-" * 40)
        else:
            print(f"No price info found for Product ID: {product_id}")
    except Exception as e:
        print(f"Error fetching price for {product_id}: {e}")

if __name__ == "__main__":
    # Test with any Croma Product ID, e.g. 312576 (Vivo V30 12GB/256GB)
    test_product_ids = ["312576", "302354", "231568"]  # Add more IDs to test
    for pid in test_product_ids:
        fetch_price(pid)
