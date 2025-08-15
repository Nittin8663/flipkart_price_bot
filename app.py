import time 
import json
import threading
import requests
from flask import Flask, render_template_string, request, redirect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Load configs
with open("config.json") as f:
    config = json.load(f)

TELEGRAM_BOT_TOKEN = config["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = config["TELEGRAM_CHAT_ID"]
CHECK_INTERVAL = config["CHECK_INTERVAL"]

app = Flask(__name__)

# HTML Template for main page
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Flipkart Price Alert</title>
<style>
body { font-family: Arial; margin: 40px; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
th { background-color: #f2f2f2; }
input[type=text], input[type=number] { width: 100%; padding: 5px; }
button { padding: 5px 10px; }
</style>
</head>
<body>
<h2>Flipkart Price Alert Bot</h2>
<table>
<tr><th>Name</th><th>URL</th><th>Target Price</th><th>Target Bundle Discount</th><th>Enabled</th><th>Actions</th></tr>
{% for p in products %}
<tr>
<td>{{ p.name }}</td>
<td><a href="{{ p.url }}" target="_blank">Link</a></td>
<td>{{ p.target_price }}</td>
<td>{{ p.get('target_bundle_discount', '-') }}</td>
<td>{{ '✅' if p.enabled else '❌' }}</td>
<td>
<a href="/toggle/{{ loop.index0 }}">Toggle</a> |
<a href="/delete/{{ loop.index0 }}">Delete</a> |
<a href="/edit/{{ loop.index0 }}">Edit</a>
</td>
</tr>
{% endfor %}
</table>
<h3>Add New Product</h3>
<form method="post" action="/add">
<input type="text" name="name" placeholder="Product Name" required>
<input type="text" name="url" placeholder="Flipkart URL" required>
<input type="number" name="target_price" placeholder="Target Price" required>
<input type="number" name="target_bundle_discount" placeholder="Target Bundle Discount (optional)">
<button type="submit">Add</button>
</form>
</body>
</html>
"""

# HTML Template for editing product
EDIT_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Edit Product</title>
<style>
body { font-family: Arial; margin: 40px; }
input[type=number], input[type=text] { width: 100%; padding: 5px; }
button { padding: 5px 10px; }
</style>
</head>
<body>
<h2>Edit Product: {{ product.name }}</h2>
<form method="post" action="/edit/{{ index }}">
<input type="text" name="name" value="{{ product.name }}" required>
<input type="text" name="url" value="{{ product.url }}" required>
<input type="number" name="target_price" value="{{ product.target_price }}" required>
<input type="number" name="target_bundle_discount" value="{{ product.get('target_bundle_discount', '') }}" placeholder="Target Bundle Discount (optional)">
<button type="submit">Save</button>
</form>
</body>
</html>
"""

def load_products():
    with open("products.json") as f:
        return json.load(f)

def save_products(products):
    with open("products.json", "w") as f:
        json.dump(products, f, indent=4)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

def get_price_and_bundle_discount(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)

    price = None
    bundle_discount = None

    try:
        price_element = driver.find_element(By.CSS_SELECTOR, "div.Nx9bqj.CxhGGd")
        price_text = price_element.text.replace("₹", "").replace(",", "")
        price = int(price_text)
    except:
        pass

    try:
        # “Save extra on buying these together” section
        bundle_element = driver.find_element(By.XPATH, "//div[contains(text(),'Save extra on buying these together')]/following-sibling::div//span[contains(@class,'_30jeq3')]")
        bundle_text = bundle_element.text.replace("₹","").replace(",","")
        bundle_discount = int(bundle_text)
    except:
        pass

    driver.quit()
    return price, bundle_discount

def price_checker():
    while True:
        products = load_products()
        for product in products:
            if not product["enabled"]:
                continue
            print(f"Checking price for: {product['url']}")
            price, bundle_discount = get_price_and_bundle_discount(product["url"])
            if price:
                print(f"Current price: ₹{price}")
                if price <= product["target_price"]:
                    send_telegram_message(f"Price Alert! {product['name']} is ₹{price}\n{product['url']}")
            if bundle_discount and product.get("target_bundle_discount"):
                print(f"Current bundle discount: ₹{bundle_discount}")
                if bundle_discount >= product["target_bundle_discount"]:
                    send_telegram_message(f"Bundle Discount Alert! {product['name']} has a discount of ₹{bundle_discount}\n{product['url']}")
        time.sleep(CHECK_INTERVAL)

@app.route("/")
def index():
    products = load_products()
    return render_template_string(HTML, products=products)

@app.route("/add", methods=["POST"])
def add():
    products = load_products()
    target_bundle_discount = request.form.get("target_bundle_discount")
    products.append({
        "name": request.form["name"],
        "url": request.form["url"],
        "target_price": int(request.form["target_price"]),
        "target_bundle_discount": int(target_bundle_discount) if target_bundle_discount else None,
        "enabled": True
    })
    save_products(products)
    return redirect("/")

@app.route("/delete/<int:index>")
def delete(index):
    products = load_products()
    products.pop(index)
    save_products(products)
    return redirect("/")

@app.route("/toggle/<int:index>")
def toggle(index):
    products = load_products()
    products[index]["enabled"] = not products[index]["enabled"]
    save_products(products)
    return redirect("/")

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    products = load_products()
    if request.method == "POST":
        products[index]["name"] = request.form["name"]
        products[index]["url"] = request.form["url"]
        products[index]["target_price"] = int(request.form["target_price"])
        tbd = request.form.get("target_bundle_discount")
        products[index]["target_bundle_discount"] = int(tbd) if tbd else None
        save_products(products)
        return redirect("/")
    else:
        return render_template_string(EDIT_HTML, product=products[index], index=index)

if __name__ == "__main__":
    threading.Thread(target=price_checker, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
