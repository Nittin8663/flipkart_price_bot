import requests

url = "https://api.croma.com/offer/allchannels/v2/detail"
headers = {
    "accept": "application/json, text/plain, */*",
    "client_id": "CROMA-WEB-APP",
    "content-type": "application/json",
    "origin": "https://www.croma.com",
    "referer": "https://www.croma.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "cookie": "bm_sz=E34C559B71544136AD569FD5D03D6A9A~YAAQFXBWuNetTquYAQAAmzFvwxw1mK8Y+yrw4TUst4I9ez9LrqTQAfd73yC7i1NQIlPxXBCNlqFIdB653A8qbXV6eVPECJ2wHIDODARM22ptAg6Ow3dHjiJvTCRaZq+/wNVi5ONZKWw3s+YrxFXhpUHydTSGnFD5qHJbf4o6fYK3h97yaXBQidhJ/UZCLrbNifeTU5/039utdHMpbkipbvkMQmRViLUunmUNGGjF31Zq8lXVVGUzcuMjjGYM1mTMeIP/jdPMbKbGEAqlkJcz8SY0TiyJf+2jogL+0jYj0o3Hmai7g15hdhssTYDUvCVsVabuPOorPb+KjspDSgZaJZqo1oLmxLj+2udn9Lf295Ur3koW6A==~4600118~4599861; Domain=.croma.com; Path=/; Expires=Tue, 19 Aug 2025 21:45:00 GMT; Max-Age=14399"
}
payload = {
    "skuId": "312576",     # Product id
    "channel": "EC",
    "storeId": "",
    "pincode": ""
}

r = requests.post(url, headers=headers, json=payload)
print("Status:", r.status_code)
print("Response:", r.text)
