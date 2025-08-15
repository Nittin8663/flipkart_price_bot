import json
import time
import threading
import requests
from flask import Flask, render_template_string
from datetime import datetime

# Load config and products
with open("config.json", "r") as f:
    CONFIG = json.load(f)

with open("products.json", "r") as f:
    PRODUCTS = json.load(f)

TELEGRAM_BOT_TOKEN = CONFIG["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = CONFIG["TELEGRAM_CHAT_ID"]
CHECK_INTERVAL = CONFIG.get("CHECK_INTERVAL", 3600)

# Flask app
app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Croma Price Tracker</title>
    <style>
        body { font-family: Arial; background: #f4f4f4; padding: 20px; }
        table { border-collapse: collapse; width: 100%; background: white; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: center; }
        th { background-color: #4CAF50; color: white; }
    </style>
</head>
<body>
    <h1>Croma Price Tracker</h1>
    <p>Last Updated: {{ last_updated }}</p>
    <table>
        <tr>
            <th>Product Name</th>
            <th>MRP</th>
            <th>Selling Price</th>
            <th>Discount</th>
        </tr>
        {% for product in prices %}
        <tr>
            <td>{{ product.name }}</td>
            <td>{{ product.mrp }}</td>
            <td>{{ product.selling_price }}</td>
            <td>{{ product.discount }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# Price fetching function
def fetch_price(product_id):
    url = f"https://api.croma.com/pricing-services/v1/price?productList={product_id}"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "channel": "EC",
        "origin": "https://www.croma.com",
        "referer": "https://www.croma.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
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

# Telegram notification
def send_telegram_message(message):
    try:
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
        requests.post(telegram_url, data=payload)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

# Background task
def price_checker():
    while True:
        messages = []
        for product in PRODUCTS:
            price_data = fetch_price(product["id"])
            if price_data:
                messages.append(f"📦 {product['name']}\n💰 {price_data['selling_price']} (MRP: {price_data['mrp']}, Discount: {price_data['discount']})")
        if messages:
            send_telegram_message("\n\n".join(messages))
        time.sleep(CHECK_INTERVAL)

# Web route
@app.route("/")
def home():
    prices = []
    for product in PRODUCTS:
        price_data = fetch_price(product["id"])
        if price_data:
            prices.append({
                "name": product["name"],
                "mrp": price_data["mrp"],
                "selling_price": price_data["selling_price"],
                "discount": price_data["discount"]
            })
    return render_template_string(HTML_TEMPLATE, prices=prices, last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    threading.Thread(target=price_checker, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
