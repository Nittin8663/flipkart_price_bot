import requests

# ----------- Proxy details -----------
proxy_username = "1258bd9e03f80533eb38__cr.in"
proxy_password = "ca69cf1263c65d0e"
proxy_host = "74.81.81.81"
proxy_port = "823"

proxies = {
    "http": f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}",
    "https": f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}",
}

# ----------- API Endpoint -----------
url = "https://api.tatadigital.com/getApplicablePromotion/getApplicationPromotionsForItemOffer"

# ----------- Headers -----------
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,hi;q=0.8,de;q=0.7",
    "authorization": "8Tksadcs85ad4vsasfasgf4sJHvfs4NiKNKLHKLH582546f646",
    "client_id": "CROMA",
    "content-type": "application/json",
    "origin": "https://www.croma.com",
    "referer": "https://www.croma.com/",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}

# ----------- Cookies -----------
cookies = {
    "ak_bmsc": "0569BC54337442B34C7247033EFAEA11~000000000000000000000000000000~YAAQnGnDF5lIiLSYAQAAhG/Evhz9BluBJhq5SCDwQFOvKHAtsg37TKl8gFNoErBvSQSwd3Fx2R1dmzmk2T9SZCmdGA47t9RsJo/iRn8etl0tdF/oy33snlPTisxwB5Dh5vxDHYBM410SyWTYmp2ZmDwl6TZBVvQIaAMO/uv4mS0mzFMHnSBbT2eQB6SSV7evRNkMKmG6FksTxsK/bsaaKl3twHp4L46OpJe1y7DEnurlt1qweRBmQmJjggmeQDiN5K9Ii9+N1x+k2BZAxdQmLT9KictgSXFvof9oT4lA1z85vjRCoHRYRWQZFChafHHc4/6sh1Kw4Q3qVYujcbaVNj4IQA8CXAxzCa6uL2N1ilmOZ/3gr+gfor/g23ea5jCirZopgHiNGkpLc6zMMli5804BSx74/ZS2MZF8N9BTRzTfwHRzh7FLtIJZOQ==",
    "bm_sz": "68E699DF5F994E3702E35CEA80C9C230~YAAQnGnDF5pIiLSYAQAAhG/EvhyMyPiOBIfn55yNRxePMBx7BwYOxiri1N81qVTViTbXqv3afgCxaSR+KnQX/0UGafl2FioEpFHI4cirWbZGNb6RREOQ7VrMMP72FkqOAdj4na5faM35sqVZ7YaDJBQIBdzizvY9QygPX7Ulh0HuHGEwjIyiC7deo1Wi8WdvtS7qQ1P/j4q4weHUGMkkv1zybzu9WYW/7E9ilRkcsu9rPhG3uELA/UcOcvLtr9FmrjSkv6Ro6ZgQ+6O7V0LesZ422z+9QZPXVXX2yDuVvRXjE5RCaQQSNJB9JGefF4E2XeApSAwAqK3IxlAVMcbMjX0Oma4S2BxCrOc5MGI4mFKWVP7UcoPlsTTYoLF88Vx9xC8qafgm5WMk5ovKlxX6qHwl/EsnOw=="
}

# ----------- Payload (from your request) -----------
payload = {
    "getApplicablePromotionsForItemRequest": {
        "itemId": "314075",
        "programId": "01eae2ec-0576-1000-bbea-86e16dcb4b79",
        "channelIds": ["TCPCHS0003"],
        "status": "ACTIVE"
    }
}

# ----------- Request & Response Handling -----------
try:
    response = requests.post(
        url,
        headers=headers,
        cookies=cookies,
        json=payload,
        proxies=proxies,
        timeout=20
    )
    print("Status code:", response.status_code)
    print("Raw response:")
    print(response.text)
    try:
        offers = response.json()
        print("\n--- Promotions ---")
        for promo in offers.get("promotions", []):
            print("Offer Name:", promo.get("promotionName"))
            print("Discount:", promo.get("discountAmount"))
            print("Description:", promo.get("description"))
            print("---")
    except Exception as e:
        print("Response is not JSON:", e)
except Exception as e:
    print("Request failed:", e)
