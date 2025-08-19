import requests

def get_croma_price(product_id):
    url = f"https://api.croma.com/pricing-services/v1/price?productList={product_id}"
    headers = {
        "accept": "application/json, text/plain, */*",
        "origin": "https://www.croma.com",
        "referer": "https://www.croma.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    print("Status Code:", r.status_code)
    if r.status_code == 200:
        try:
            data = r.json()
            priceinfo = data.get("pricelist", [{}])[0]
            print("Product ID:", priceinfo.get("productId"))
            print("MRP:", priceinfo.get("mrp"))
            print("Selling Price:", priceinfo.get("sellingPriceValue"))
            print("Discount %:", priceinfo.get("discountPercentage"))
        except Exception as e:
            print("JSON Error:", e)
            print("Response Text:", r.text)
    else:
        print("Error Response:", r.text)

if __name__ == "__main__":
    product_id = "312576"  # Yahan apna product id daalein
    get_croma_price(product_id)
