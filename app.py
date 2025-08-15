import re
import json
import time
import threading
from datetime import datetime
from pathlib import Path

import requests
from flask import Flask, request, redirect, url_for, render_template_string, abort

# ---------- Files ----------
CONFIG_PATH = Path("config.json")
PRODUCTS_PATH = Path("products.json")

# ---------- Load config ----------
if not CONFIG_PATH.exists():
    raise SystemExit("config.json not found.")
with CONFIG_PATH.open("r", encoding="utf-8") as f:
    CONFIG = json.load(f)

TELEGRAM_BOT_TOKEN = CONFIG.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = CONFIG.get("TELEGRAM_CHAT_ID", "")
CHECK_INTERVAL = int(CONFIG.get("CHECK_INTERVAL", 3600))

# ---------- Flask app ----------
app = Flask(__name__)

# Thread-safety for file operations
_products_lock = threading.Lock()

# In-memory cache: latest price data + alert memory to avoid spamming
latest_prices = {}        # key: product_id -> dict with mrp/selling/discount/time
last_alert_price = {}     # key: product_id -> last selling price (int) we alerted at

# ---------- Croma API ----------
CROMA_PRICE_URL = "https://api.croma.com/pricing-services/v1/price?productList={pid}"
CROMA_HEADERS = {
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
    # UA similar to your browser is important to avoid 403
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/139.0.0.0 Safari/537.36",
}

# If ever needed for stubborn 403s, you can add your browser cookie here dynamically:
# CROMA_HEADERS["cookie"] = "bm_sz=...; another_cookie=..."


# ---------- Helpers ----------
def load_products():
    """Load products.json safely."""
    if not PRODUCTS_PATH.exists():
        return []
    with _products_lock:
        with PRODUCTS_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
            # Normalize schema (ensure keys)
            for p in data:
                p.setdefault("name", "")
                p.setdefault("id", "")
                p.setdefault("target_price", 0)
                p.setdefault("enabled", True)
            return data


def save_products(data):
    """Write products.json safely."""
    with _products_lock:
        with PRODUCTS_PATH.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


def parse_int_price(any_price_str):
    """Convert '₹11,499.00' or '11499' to int 11499."""
    if any_price_str is None:
        return None
    digits = re.sub(r"[^\d]", "", str(any_price_str))
    return int(digits) if digits else None


def fetch_price_from_croma(product_id):
    """Call Croma pricing API for one product id; return dict or None."""
    try:
        url = CROMA_PRICE_URL.format(pid=product_id)
        r = requests.get(url, headers=CROMA_HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        # Expected: {"pricelist":[{...}]}
        lst = data.get("pricelist", [])
        if not lst:
            return None
        item = lst[0]
        return {
            "mrp": item.get("mrp"),
            "selling_price": item.get("sellingPrice"),
            "discount": item.get("discountPercentage"),
        }
    except Exception as e:
        print(f"Error fetching price for {product_id}: {e}")
        return None


def send_telegram_message(text):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print("Telegram error:", e)


def check_and_alert_loop():
    """Background worker: periodically checks prices & alerts on target match."""
    while True:
        products = load_products()
        for p in products:
            if not p.get("enabled", True):
                continue

            pid = str(p.get("id", "")).strip()
            if not pid:
                continue

            price_data = fetch_price_from_croma(pid)
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if price_data:
                latest_prices[pid] = {
                    "name": p.get("name", pid),
                    "mrp": price_data["mrp"],
                    "selling_price": price_data["selling_price"],
                    "discount": price_data["discount"],
                    "time": ts,
                    "target_price": p.get("target_price", 0),
                    "enabled": p.get("enabled", True),
                }

                sp_int = parse_int_price(price_data["selling_price"])
                target = int(p.get("target_price", 0) or 0)

                # Alert only when price <= target and we haven't alerted for this exact price
                if target > 0 and sp_int is not None and sp_int <= target:
                    prev_alert = last_alert_price.get(pid)
                    if prev_alert != sp_int:
                        last_alert_price[pid] = sp_int
                        msg = (
                            f"🔥 Target hit!\n"
                            f"{p.get('name', pid)}\n"
                            f"Selling: {price_data['selling_price']}  |  "
                            f"MRP: {price_data['mrp']}  |  "
                            f"Discount: {price_data['discount']}\n"
                            f"Target: ₹{target:,}"
                        )
                        send_telegram_message(msg)
            else:
                # Keep a minimal entry if fetch failed
                latest_prices[pid] = {
                    "name": p.get("name", pid),
                    "mrp": "N/A",
                    "selling_price": "N/A",
                    "discount": "N/A",
                    "time": ts,
                    "target_price": p.get("target_price", 0),
                    "enabled": p.get("enabled", True),
                    "error": "Fetch failed",
                }

        time.sleep(max(15, CHECK_INTERVAL))  # at least 15s between rounds


# ---------- HTML ----------
PAGE_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Croma Price Alert</title>
  <meta http-equiv="refresh" content="60"> <!-- auto-refresh every 60s -->
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; background:#f7f7f9; }
    h1 { margin: 0 0 16px; color:#0366d6; }
    table { width:100%; border-collapse: collapse; background:#fff; }
    th, td { padding:10px; border:1px solid #eaecef; text-align:center; }
    th { background:#f1f8ff; }
    .actions a, .actions button { margin: 0 4px; text-decoration:none; }
    form.inline { display:inline; }
    .container { background:#fff; padding:16px; border:1px solid #eaecef; border-radius:8px; }
    .grid { display:grid; grid-template-columns: 1fr 1fr; gap:16px; }
    .muted { color:#666; font-size:12px; }
    .badge-on { background:#28a745; color:#fff; padding:2px 8px; border-radius:12px; font-size:12px; }
    .badge-off{ background:#d73a49; color:#fff; padding:2px 8px; border-radius:12px; font-size:12px; }
    input, button { padding:8px; }
    input[type="number"]{ width:120px; }
    .nowrap{ white-space:nowrap; }
  </style>
</head>
<body>
  <h1>Croma Price Alert</h1>

  <div class="container" style="margin-bottom:16px;">
    <h3 style="margin-top:0;">Add Product</h3>
    <form method="post" action="{{ url_for('add_product') }}">
      <label>Product ID:</label>
      <input name="id" required />
      <label> Name:</label>
      <input name="name" required style="width:320px;" />
      <label> Target Price (₹):</label>
      <input name="target_price" type="number" min="0" step="1" required />
      <button type="submit">Add</button>
    </form>
    <div class="muted">Hint: Product ID is the numeric code (e.g., 315011). We fetch live price from Croma API.</div>
  </div>

  <div class="container">
    <div class="grid">
      <div><strong>Total Products:</strong> {{ products|length }}</div>
      <div style="text-align:right;"><span class="muted">Auto-refreshes every 60s</span></div>
    </div>

    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th class="nowrap">Product ID</th>
          <th>MRP</th>
          <th>Selling</th>
          <th>Discount</th>
          <th>Target (₹)</th>
          <th>Status</th>
          <th>Last Checked</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
      {% for p in products %}
        {% set lp = latest.get(p.id) %}
        <tr>
          <td>{{ p.name }}</td>
          <td class="nowrap">{{ p.id }}</td>
          <td>{{ lp.mrp if lp else '—' }}</td>
          <td>{{ lp.selling_price if lp else '—' }}</td>
          <td>{{ lp.discount if lp else '—' }}</td>
          <td>{{ p.target_price }}</td>
          <td>
            {% if p.enabled %}
              <span class="badge-on">Enabled</span>
            {% else %}
              <span class="badge-off">Disabled</span>
            {% endif %}
          </td>
          <td>{{ lp.time if lp else '—' }}</td>
          <td class="actions">
            <form class="inline" method="post" action="{{ url_for('toggle_product', product_id=p.id) }}">
              <button type="submit">{{ 'Disable' if p.enabled else 'Enable' }}</button>
            </form>
            <form class="inline" method="get" action="{{ url_for('edit_product_form', product_id=p.id) }}">
              <button type="submit">Edit</button>
            </form>
            <form class="inline" method="post" action="{{ url_for('delete_product', product_id=p.id) }}"
                  onsubmit="return confirm('Delete this product?');">
              <button type="submit">Delete</button>
            </form>
          </td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
  </div>
</body>
</html>
"""

EDIT_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Edit Product</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; background:#f7f7f9; }
    .container { background:#fff; padding:16px; border:1px solid #eaecef; border-radius:8px; max-width:640px; }
    input, button { padding:8px; }
    label { display:block; margin-top:8px; }
  </style>
</head>
<body>
  <div class="container">
    <h2>Edit Product</h2>
    <form method="post" action="{{ url_for('edit_product', product_id=product.id) }}">
      <label>Product ID</label>
      <input name="id" value="{{ product.id }}" required />

      <label>Name</label>
      <input name="name" value="{{ product.name }}" required style="width: 100%;" />

      <label>Target Price (₹)</label>
      <input name="target_price" type="number" min="0" step="1" value="{{ product.target_price }}" required />

      <label>Enabled</label>
      <select name="enabled">
        <option value="true"  {{ 'selected' if product.enabled else '' }}>True</option>
        <option value="false" {{ '' if product.enabled else 'selected' }}>False</option>
      </select>

      <div style="margin-top:12px;">
        <button type="submit">Save</button>
        <a href="{{ url_for('home') }}" style="margin-left:8px;">Cancel</a>
      </div>
    </form>
  </div>
</body>
</html>
"""

# ---------- Routes ----------
@app.route("/")
def home():
    products = load_products()
    # make a simple structure for template
    prods_for_tpl = []
    for p in products:
        prods_for_tpl.append(type("P", (), {
            "id": str(p.get("id", "")),
            "name": p.get("name", ""),
            "target_price": int(p.get("target_price", 0) or 0),
            "enabled": bool(p.get("enabled", True))
        }))
    return render_template_string(PAGE_HTML, products=prods_for_tpl, latest=latest_prices)


@app.route("/add", methods=["POST"])
def add_product():
    pid = (request.form.get("id") or "").strip()
    name = (request.form.get("name") or "").strip()
    target_price = int(request.form.get("target_price") or 0)
    if not pid or not name:
        abort(400, "Invalid input")

    products = load_products()
    # prevent duplicates by id
    for p in products:
        if str(p.get("id")) == pid:
            abort(400, "Product with this ID already exists.")

    products.append({
        "id": pid,
        "name": name,
        "target_price": target_price,
        "enabled": True
    })
    save_products(products)
    return redirect(url_for("home"))


@app.route("/toggle/<product_id>", methods=["POST"])
def toggle_product(product_id):
    products = load_products()
    found = False
    for p in products:
        if str(p.get("id")) == str(product_id):
            p["enabled"] = not p.get("enabled", True)
            found = True
            break
    if not found:
        abort(404, "Product not found")
    save_products(products)
    return redirect(url_for("home"))


@app.route("/delete/<product_id>", methods=["POST"])
def delete_product(product_id):
    products = load_products()
    new_list = [p for p in products if str(p.get("id")) != str(product_id)]
    if len(new_list) == len(products):
        abort(404, "Product not found")
    save_products(new_list)
    # also clear alert memory for that id
    last_alert_price.pop(str(product_id), None)
    latest_prices.pop(str(product_id), None)
    return redirect(url_for("home"))


@app.route("/edit/<product_id>", methods=["GET"])
def edit_product_form(product_id):
    products = load_products()
    for p in products:
        if str(p.get("id")) == str(product_id):
            # simple object for template
            obj = type("P", (), {
                "id": str(p.get("id", "")),
                "name": p.get("name", ""),
                "target_price": int(p.get("target_price", 0) or 0),
                "enabled": bool(p.get("enabled", True))
            })
            return render_template_string(EDIT_HTML, product=obj)
    abort(404, "Product not found")


@app.route("/edit/<product_id>", methods=["POST"])
def edit_product(product_id):
    new_id = (request.form.get("id") or "").strip()
    name = (request.form.get("name") or "").strip()
    target_price = int(request.form.get("target_price") or 0)
    enabled_str = (request.form.get("enabled") or "true").lower()
    enabled = enabled_str == "true"

    products = load_products()

    # If changing ID, ensure no collision
    if new_id != product_id:
        for p in products:
            if str(p.get("id")) == new_id:
                abort(400, "Another product already uses this new ID.")

    updated = False
    for p in products:
        if str(p.get("id")) == str(product_id):
            p["id"] = new_id
            p["name"] = name
            p["target_price"] = target_price
            p["enabled"] = enabled
            updated = True
            break

    if not updated:
        abort(404, "Product not found")

    save_products(products)

    # If ID changed, move caches
    if new_id != product_id:
        latest_prices[new_id] = latest_prices.pop(product_id, latest_prices.get(new_id, {}))
        last_alert_price[new_id] = last_alert_price.pop(product_id, last_alert_price.get(new_id, None))

    return redirect(url_for("home"))


# ---------- Startup ----------
if __name__ == "__main__":
    # Start background checker
    threading.Thread(target=check_and_alert_loop, daemon=True).start()
    # Run server
    app.run(host="0.0.0.0", port=5000, debug=True)
