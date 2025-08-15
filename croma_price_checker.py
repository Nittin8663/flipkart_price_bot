import requests

def fetch_price(product_id):
    url = f"https://api.croma.com/pricing-services/v1/price?productList={product_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # HTTP error raise karega

        data = response.json()

        # Price extract karna
        if "productList" in data and len(data["productList"]) > 0:
            price = data["productList"][0].get("price")
            currency = data["productList"][0].get("currency", "INR")
            print(f"Product ID {product_id} Price: {currency} {price}")
        else:
            print(f"Price not found for Product ID {product_id}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching price for Product ID {product_id}: {e}")

# --- Test Script ---
if __name__ == "__main__":
    # Test product IDs (example)
    test_product_ids = ["315011", "315012", "315013"]

    for pid in test_product_ids:
        fetch_price(pid)
