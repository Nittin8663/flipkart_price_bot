import requests

url = "https://api.tatadigital.com/api/v1/commerce/rich-content/internal/get-data?productId=312576&fields=FULL&pageType=ContentPage"

headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,hi;q=0.8,de;q=0.7",
    "content-type": "application/json",
    "neu-app-version": "6.1.0",
    "origin": "https://www.tataneu.com",
    "referer": "https://www.tataneu.com/",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}

try:
    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )
    print("Status code:", response.status_code)
    print("Raw response:")
    print(response.text)
    try:
        data = response.json()
        print("\n--- Parsed Data ---")
        print("Top-level keys:", list(data.keys()))
        # For deep inspection, uncomment below:
        # import json
        # print(json.dumps(data, indent=2))
    except Exception as e:
        print("Response is not JSON:", e)
except Exception as e:
    print("Request failed:", e)
