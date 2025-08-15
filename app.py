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

HTML = """..."""  # keep your previous HTML templates

EDIT_HTML = """..."""  # keep your previous edit template

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

def get_price_and_bundle(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 13) Mobile")  # mobile user-agent
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)

    price = None
    bundle_text = None

    try:
        # Price selector for mobile site
        price_element = driver.find_element(By.CSS_SELECTOR, "div._30jeq3._16Jk6d")
        price_text = price_element.text.replace("₹", "").replace(",", "")
        price = int(price_text)
    except:
        price = None

    try:
        # Bundle / Buy Together offer selector (mobile site)
        bundle_element = driver.find_element(By.XPATH, "//div[contains(text(),'Buy Together') or contains(text(),'Bundle Offer')]")
        bundle_text = bundle_element.text
    except:
        bundle_text = None

    driver.quit()
    return price, bundle_text

def price_checker():
    while True:
        products = load_products()
        for product in products:
            if not product["enabled"]:
                continue
            print(f"Checking price for: {product['name']}")
            price, bundle = get_price_and_bundle(product["url"])
            if price:
                print(f"Current price: ₹{price}")
                if price <= product["target_price"]:
                    msg = f"Price Alert! {product['name']} is ₹{price}\n{product['url']}"
                    if bundle:
                        msg += f"\nBundle Offer: {bundle}"
                    send_telegram_message(msg)
        time.sleep(CHECK_INTERVAL)

# Flask routes same as before
@app.route("/")
def index():
    products = load_products()
    return render_template_string(HTML, products=products)

@app.route("/add", methods=["POST"])
def add():
    products = load_products()
    products.append({
        "name": request.form["name"],
        "url": request.form["url"],
        "target_price": int(request.form["target_price"]),
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
        products[index]["target_price"] = int(request.form["target_price"])
        save_products(products)
        return redirect("/")
    else:
        return render_template_string(EDIT_HTML, product=products[index], index=index)

if __name__ == "__main__":
    threading.Thread(target=price_checker, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
