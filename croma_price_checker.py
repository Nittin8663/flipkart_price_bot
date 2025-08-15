import requests

def fetch_price():
    url = "https://api.croma.com/pricing-services/v1/price?productList=315011"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "channel": "WEB"  # This is the required header
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors

        data = response.json()
        print("Response Data:", data)  # Inspect the full response

        # Extract price if available
        if "productList" in data and data["productList"]:
            product = data["productList"][0]
            price = product.get("price", "Price not available")
            currency = product.get("currency", "INR")
            print(f"Product ID 315011 Price: {currency} {price}")
        else:
            print("Price not found for Product ID 315011")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching price: {e}")

if __name__ == "__main__":
    fetch_price()
