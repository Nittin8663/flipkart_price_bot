import json
import time
import threading
import requests
from flask import Flask, render_template_string
from datetime import datetime

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

with open("products.json", "r") as f:
    products = json.load(f)

TELEGRAM_BOT_TOKEN = config["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = config["TELEGRAM_CHAT_ID"]
CHECK_INTERVAL = config["CHECK_INTERVAL"]

# Headers (from browser Network tab)
HEADERS = {
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
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}

app = Flask(__name__)
latest_prices = {}

def fetch_price(product_id):
    url = f"https://api.croma.com/pricing-services/v1/price?productList={product_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        if "pricelist" in data and len(data["pricelist"]) > 0:
            item = data["pricelist"][0]
            return {
                "mrp": item["mrp"],
                "selling_price": item["sellingPrice"],
                "discount": item["discountPercentage"]
            }
    except Exception as e:
        print(f"Error fetching price for {product_id}: {e}")
    return None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def check_prices():
    global latest_prices
    while True:
        for product in products:
            price_data = fetch_price(product["id"])
            if price_data:
                latest_prices[product["id"]] = {
                    "name": product["name"],
                    "mrp": price_data["mrp"],
                    "selling_price": price_data["selling_price"],
                    "discount": price_data["discount"],
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                msg = (
                    f"{product['name']}\n"
                    f"MRP: {price_data['mrp']}\n"
                    f"Selling Price: {price_data['selling_price']}\n"
                    f"Discount: {price_data['discount']}"
                )
                send_telegram_message(msg)
        time.sleep(CHECK_INTERVAL)

# HTML Template inline
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Croma Price Tracker</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f8f8f8; }
        h1 { text-align: center; }
        table { border-collapse: collapse; width: 100%; background: white; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        th { background-color: #4CAF50; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Croma Price Tracker</h1>
    <table>
        <tr>
            <th>Product</th>
            <th>MRP</th>
            <th>Selling Price</th>
            <th>Discount</th>
            <th>Last Updated</th>
        </tr>
        {% for pid, data in prices.items() %}
        <tr>
            <td>{{ data.name }}</td>
            <td>{{ data.mrp }}</td>
            <td>{{ data.selling_price }}</td>
            <td>{{ data.discount }}</td>
            <td>{{ data.time }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, prices=latest_prices)

if __name__ == "__main__":
    threading.Thread(target=check_prices, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
