import requests

proxies = {
    "http": "http://1258bd9e03f80533eb38__cr.in:ca69cf1263c65d0e@gw.dataimpulse.com:10000",
    "https": "http://1258bd9e03f80533eb38__cr.in:ca69cf1263c65d0e@gw.dataimpulse.com:10000",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/115.0.0.0 Safari/537.36"
}

url = "https://www.croma.com/"
r = requests.get(url, headers=headers, proxies=proxies, timeout=15)
print(r.status_code)
print(r.text[:500])
