import requests

url = "https://api.croma.com/pricing-services/v1/price?productList=312576"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,hi;q=0.8,de;q=0.7",
    "channel": "EC",
    "origin": "https://www.croma.com",
    "referer": "https://www.croma.com/",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}

cookies = {
    "bm_sz": "D4EE8A6BE999499542A67F183BE205C0~YAAQVHBWuFunkLCYAQAADfqTxhwI03dyq4TJOmAGnbciyWUd09tnBudoBilB4nOcMbcDaCFAwj3Af38iMfCmQLFdxH7aGMg7EgCVfNx1KGe1qPSDMP1M862BvRejKNfOiCgTwrUzdlR8+LXx92+DGOEerpsaTOqPEXihn2jpUuzQXfJS2K4WV4Zm4UbPws326d2JKhK8+T7yOG15SAho18UdF5aUoX0hUlAgsKzxgRAbwZFwqzF7U5tOKbYFqbm/yaUKg0W4n/Kxm7Vc0FVHSuzch/0uOXAs5QNpqUuasiAqq7wCu7HtWGZv/WWl0UqcCDHt9VZc3gK+4AAo2GClw25bgYS8DQUVRrvCgKiqBTU97pKDTMMWfPjDxV+DDqlBSJCSmYdrgdbOf9oe+lgzZA==~4273719~3618102"
}

proxies = {
    "http": "http://1258bd9e03f80533eb38__cr.in:ca69cf1263c65d0e@74.81.81.81:823",
    "https": "http://1258bd9e03f80533eb38__cr.in:ca69cf1263c65d0e@74.81.81.81:823",
}

r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies, timeout=20)
print(r.status_code)
print(r.text)
