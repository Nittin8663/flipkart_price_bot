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

cookies = {
    "ak_bmsc": "F93D798EAFF5E49A4F02924893E6E888~000000000000000000000000000000~YAAQXXBWuDC2pMaYAQAACnmmxhxuF+t762sonJoAUL7zOwOJX/A+AF88r9oj8uy8dgwn0wC7vH1qrDtMSZ2nGBcRJ6U9omDmBuElYdy+iNqUKRmqKdSClKVfZ/HhGXTjXnibO9CC34t3S9z1h8knDugK8S8T224tQkLeW4LWeqngexHPwlEgmoGLM7mQImrRCdLf/zah+XevegaubVMkZlWi/FCZRBA+BNfGKABSboceBOkVtRAgoLwf4JOWxqUMrIYQMrT16mKYyM8+ns3JBHjo4bZWyUUwNKuRBfjK/jGxWTuvfhyKvgF/DkR8H/kyqaYYt82fAdLdKs/qRo4Dl//6PhZSDYVh4WZpa5WVeH5qA9mIGEb6WQpysmxj0F1hnOT1ohHBoZk1x0UUTEnDNaE4HK7w50Osd3wnwylvab9Cbh9gzICKwXtO6g==",
    "bm_sz": "5FC9E74C9F3EA793B81071CF2D41F5F4~YAAQXXBWuDG2pMaYAQAACnmmxhwDmDNdOGOITIMAUw8Si2Pmz7sKqD0PKIiO3cmuVEXm+suMGgjPUsQfSiPSfGVkkUZJolNrqfeH8AQxwKV+kNxGeMwdih9grVyeUrQgVycx0V8wcS348aDdNLtYJjVCGtq7oSqGZIoS71zVoUN/xVIw0xBUb2mDL47+Ra1gSyhR2E/cV9vYWXQuVgUouPpZRjd9KdUj7hXJvqZA8tCiLJvGJtRpgOY7tx8KaROaUlPa4DEd1OV0JfsOixPqZq5gm6//lkHvlYAupJzenRS8e0PwENLdtz4yX2igpyfURk8ytTwOeprlzUfGzkRTqY5ItJDnLQiRQUNeqo7NdjqaLQZZWcc8fFdnZjyQ3ivel+tm/x9DjDG5Oa/3O2NjtAmL2fXMIw==~4473667~4470854"
}

try:
    response = requests.get(
        url,
        headers=headers,
        cookies=cookies,
        timeout=30
    )
    print("Status code:", response.status_code)
    # Print raw response, useful for debugging
    print("Raw response:")
    print(response.text)
    try:
        data = response.json()
        print("\n--- Parsed Data ---")
        # Print top-level keys (to know structure)
        print("Top-level keys:", list(data.keys()))
        # Example: print product title if available
        # print("Title:", data.get('title'))
        # If you want to see the whole JSON neatly:
        # import json
        # print(json.dumps(data, indent=2))
    except Exception as e:
        print("Response is not JSON:", e)
except Exception as e:
    print("Request failed:", e)
