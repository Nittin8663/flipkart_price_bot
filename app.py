import json
import requests
import re
from flask import Flask, request, redirect, url_for
from threading import Thread
from datetime import datetime
import time
import os

# --- CONFIG ---
with open("config.json") as f:
    CONFIG = json.load(f)

BOT_TOKEN = CONFIG["TELEGRAM_BOT_TOKEN"]
CHAT_ID = CONFIG["TELEGRAM_CHAT_ID"]
CHECK_INTERVAL = CONFIG.get("CHECK_INTERVAL", 600)

PRODUCTS_FILE = "products.json"

app = Flask(__name__)

# --- HELPERS ---
def load_products():
    if not os.path.exists(PRODUCTS_FILE):
        return []
    with open(PRODUCTS_FILE) as f:
        return json.load(f)

def save_products(products):
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f, indent=4)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram send error: {e}")

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
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()
    if "pricelist" in data and len(data["pricelist"]) > 0:
        return data["pricelist"][0]
    return None

def fetch_promotion_offer(product_id):
    url = "https://api.tatadigital.com/getApplicablePromotion/getApplicationPromotionsForItemOffer"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "authorization": "8Tksadcs85ad4vsasfasgf4sJHvfs4NiKNKLHKLH582546f646",  # Update this from browser if needed!
        "client_id": "CROMA",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.croma.com",
        "referer": "https://www.croma.com/",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "cookie": "ak_bmsc=D3FBA7D2F179FB9DE84082AB495D7AA8~000000000000000000000000000000~YAAQHXBWuAanOr6YAQAAa1VUwxxMeBXNtaBQQjhwqY3XefAres/8H07NLYhTaYb/tB6Xkmd1vaVgJU8m0jbB6vF63NjwJW7qoS2IIy27Fs+0suiG2I9PbSYgmvhkyGYxk8UcpRGJus9ZvZV7CWWqDTLA+q5RCDknE+6YGt/oSREGf675FFUOn99pzb/CxoBaf1p0sVuOw4ATAZb9ICb6R2O9GlCVSsCtuxUXb+AL0vxEQrBVOXs0ngO42cOnzS05yH7IAQaZgHAjFUR/rAs6EJpfFXEynu0ENuVaMGq4ObcOOOOu6dFcly6+4hR/UDbXcooGRa57PlVxshKLCc8DdowbpsqPlDBsyELai40G0Vs9GKvytCzcmbA3FFp+kIQ3zorIQzqr1eNfrqLulGU34H8=; bm_sz=C7D388EDE03159AF14D145FBD3A8433C~YAAQHXBWuAenOr6YAQAAa1VUwxw1ywp/RA4JPehBTRHBG1kUDpXuqdHndtq5u67BOmreZpkyd7cSHtme+vBvlpu3tu9CBp1xSYGJZqgblmxigdI0od805KRBLsE/gNObMgLo8w5aaI526GAZd2fD+vPwI35w+W3ZE87u/1pbDi++yTLJc6oP+z6A696iW0M+4Cn08Uiqy3Od/m2cTvHb+4WFaOjk8BxWPqi8MCkIcXxhno+BxVhfEGH7mLncXkC/0aC9VqRQagBFeVnXN7sYOjepKv+CzEnia92HDo3JInoWxM7zGsW14KUNXipS98Rq995l7PiX+ccgUGVuOxiqpOnGys9SgCEINE8C/Rxs+oM3M/4lMHIVWnms0w==~4342337~4404018"
    }
    payload = {
        "skuId": product_id
    }
    try:
        r = requests.post(url, headers=headers, data=payload)
        r.raise_for_status()
        data = r.json()
        offers = []
        offer_list = (
            data.get("getApplicablePromotionsForItemResponse", {})
            .get("offerDetailsList", [])
        )
        for offer in offer_list:
            title = offer.get("offerTitle", "")
            desc = offer.get("description", "")
            match = re.search(r'Rs\.?\s?([0-9]+)', title)
            saving = float(match.group(1)) if match else 0
            offers.append({
                "title": title,
                "desc": desc,
                "saving": saving
            })
        return offers
    except Exception as e:
        print(f"Promotion fetch error: {e}")
        return []

def check_prices():
    products = load_products()
    for p in products:
        if not p.get("enabled", True):
            continue
        try:
            price_data = fetch_price(p["id"])
            if not price_data:
                continue
            mrp = price_data["mrp"]
            selling = price_data["sellingPriceValue"]
            discount = price_data["discountPercentage"]
            p["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            p["last_price"] = selling

            # --- Promotion Offer Fetch ---
            promotions = fetch_promotion_offer(p["id"])
            promo_text = ""
            promo_alert = False
            target_promotion = p.get("target_promotion")
            if promotions:
                for promo in promotions:
                    promo_text += f"\nOffer: {promo['title']} | Save: ₹{promo['saving']}"
                    # Promotion alert: if any offer saving >= target_promotion
                    if target_promotion and float(promo["saving"]) >= float(target_promotion):
                        promo_alert = True

            print(f"{p['name']}: MRP {mrp} | Selling {selling} | Discount {discount}{promo_text}")

            # Alert condition: selling price <= target OR promo saving >= target_promotion
            if (
                (p.get("target_price") and float(selling) <= float(p["target_price"]))
                or promo_alert
            ):
                send_telegram_message(
                    f"Price/Offer Alert!\n{p['name']}\nMRP: {mrp}\nPrice: ₹{selling}\nDiscount: {discount}{promo_text}"
                )

        except Exception as e:
            print(f"Error fetching price for {p['id']}: {e}")
    save_products(products)

def background_checker():
    while True:
        check_prices()
        time.sleep(CHECK_INTERVAL)

# --- ROUTES ---
@app.route("/")
def index():
    products = load_products()
    html = """
    <html>
    <head>
        <title>Price Tracker</title>
        <style>
            body { font-family: Arial; margin: 20px; background: #f4f4f4; }
            table { border-collapse: collapse; width: 100%; background: #fff; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
            th { background: #333; color: #fff; }
            a { text-decoration: none; padding: 5px 10px; border-radius: 4px; }
            .edit { background: #007bff; color: #fff; }
            .toggle { background: orange; color: #fff; }
            .delete { background: red; color: #fff; }
            .add { background: green; color: #fff; padding: 8px 12px; display: inline-block; margin-bottom: 10px; }
        </style>
    </head>
    <body>
    <h1>Price Tracker</h1>
    <a href='/add' class='add'>Add Product</a>
    <table>
    <tr>
        <th>Name</th>
        <th>Target Price</th>
        <th>Target Promotion</th>
        <th>Last Price</th>
        <th>Last Checked</th>
        <th>Status</th>
        <th>Actions</th>
    </tr>
    """
    for p in products:
        # Fetch promotion offers for display in UI
        promotions = fetch_promotion_offer(p["id"])
        promo_html = ""
        if promotions:
            for promo in promotions:
                promo_html += f"<div><b>{promo['title']}</b> <span style='color:green'>(Save: ₹{promo['saving']})</span></div>"
        html += f"""
        <tr>
            <td>{p['name']}<br>{promo_html}</td>
            <td>{p.get('target_price', '')}</td>
            <td>{p.get('target_promotion', '')}</td>
            <td>{p.get('last_price', '')}</td>
            <td>{p.get('last_checked', '')}</td>
            <td>{"Enabled" if p.get('enabled', True) else "Disabled"}</td>
            <td>
                <a href='/edit/{p['id']}' class='edit'>Edit</a>
                <a href='/toggle/{p['id']}' class='toggle'>Toggle</a>
                <a href='/delete/{p['id']}' class='delete'>Delete</a>
            </td>
        </tr>
        """
    html += "</table></body></html>"
    return html

@app.route("/edit/<product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    products = load_products()
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return "Product not found", 404

    if request.method == "POST":
        product["target_price"] = float(request.form["target_price"])
        product["target_promotion"] = float(request.form["target_promotion"])
        save_products(products)
        Thread(target=check_prices).start()
        return redirect(url_for("index"))

    return f"""
    <html><body>
    <h1>Edit {product['name']}</h1>
    <form method='POST'>
        Target Price: <input type='number' step='0.01' name='target_price' value='{product.get("target_price", "")}' required><br><br>
        Target Promotion (save amount): <input type='number' step='0.01' name='target_promotion' value='{product.get("target_promotion", "")}' required><br><br>
        <input type='submit' value='Save'>
    </form>
    </body></html>
    """

@app.route("/toggle/<product_id>")
def toggle_product(product_id):
    products = load_products()
    for p in products:
        if p["id"] == product_id:
            p["enabled"] = not p.get("enabled", True)
    save_products(products)
    return redirect(url_for("index"))

@app.route("/delete/<product_id>")
def delete_product(product_id):
    products = [p for p in load_products() if p["id"] != product_id]
    save_products(products)
    return redirect(url_for("index"))

@app.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        products = load_products()
        new_product = {
            "id": request.form["id"],
            "name": request.form["name"],
            "target_price": float(request.form["target_price"]),
            "target_promotion": float(request.form["target_promotion"]),
            "enabled": True
        }
        products.append(new_product)
        save_products(products)
        return redirect(url_for("index"))
    return """
    <html><body>
    <h1>Add Product</h1>
    <form method='POST'>
        Product ID: <input type='text' name='id' required><br><br>
        Name: <input type='text' name='name' required><br><br>
        Target Price: <input type='number' step='0.01' name='target_price' required><br><br>
        Target Promotion (save amount): <input type='number' step='0.01' name='target_promotion' required><br><br>
        <input type='submit' value='Add Product'>
    </form>
    </body></html>
    """

if __name__ == "__main__":
    Thread(target=background_checker, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
