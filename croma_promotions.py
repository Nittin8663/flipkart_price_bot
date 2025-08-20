import requests

url = "https://api.tatadigital.com/api/v2/commerce/product-offers?skuId=312576&category=electronics&pinCode=400001&categoryId=10"

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
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    # Add these if present in network request:
    "client_id": "TCP-WEB-APP",
    "client_secret": "6fe27bd7-658d-4d28-ab66-a71da9637529",
    "anonymous_id": "d46a37d0-c7e3-4db8-99c5-cbdad1c55428",
    "jarvissessionid": "e392f5e4-9dae-4cf2-8f07-9d2f04d72a6a",
    "programid": "01eae2ec-0576-1000-bbea-86e16dcb4b79",
    "request_id": "005ad92b-57d1-4ac2-96bf-0229ebdb2197",
    "x-offer-benefit-threshold": "50"
    # If 'authorization' is present, add here
}

# Paste your Cookie from browser session here
cookies = {
    "ak_bmsc": "D57222253C80FF06EF349FA4ECF318D3~000000000000000000000000000000~YAAQXXBWuCG3pMaYAQAAvHqmxhz/cYxdq2UsgYF3mgWXoZTXDAxVp/QuhFtiVG9hec37tSb02UKyjUApreUAOe/vfeY2yf+HkdTN4WTwH13SVvctzNbD4YDca5SgBsgWquCE3DbWEFfwco05XE3/+oenU7P5sMOy8Vw0AvYYr9LTXOGD2nr5ii9L/LIjdPM9PiLphdGYpNeDGwdBSNHgYEaBMsvni3uYuAFjJBX7WB+i+wky7QRXuXk3edYOnrerlSxtImdAwjtyobZoAxq1Q5UjlR3ex0pBP/rVIJ28r0YOp6vggw/EBYFmKaT9M5nNlOKdV6RVyx8llW2udPUhN6f30f/LvLW1t1a4mKUTGRxPZPO8oVxuTGogMxeOyvPesdrKW80+cffIMBCKVtUHQPECpIHAGOTbeDUKR5hkg9WOvbtLur8H8rYp4Q==",
    "bm_sz": "B5D7354A66427500FE7D0DF798F368F8~YAAQXXBWuCK3pMaYAQAAvXqmxhw8aqi38RYTbeVptAgThveRPhNxlps3rj5FYOZATqFaGscbBI4bgd8UkTq0XFx6nCebOSXkkUr9mJYTZVcTkh1lpSMViiyCGpnEyjlyy12CyWerpesVkLQBzcznCMtJCeBYpp/8nQveaqO+xOw7y1TCPNZEdPRiu/hubN/hHfdlVHIL2gLrQKuKYIAOZ+KkUT2G5TvoLM2yCnsAhvV8DTLHQtzXrMgJ49mE3belMYyMfZHOFtDBX/ipn17Qpv3jpVeuFamw9/QqJEAmB6Bvz15TiuuSkdoDX9PXd/3GnWAIHLtBEZx9XRUb86qbNAyRmnPWnt/kcq743bXSl+lppMm0njnHibTd/q6Ul94cCqAqEowjfLIa0E7e7TFac/E7Zxla6A==~4473667~4470854"
}

try:
    response = requests.get(
        url,
        headers=headers,
        cookies=cookies,
        timeout=30
    )
    print("Status code:", response.status_code)
    print("Raw response:")
    print(response.text)
    try:
        data = response.json()
        print("\n--- Parsed Offers ---")
        # Print all offer details (customize as needed)
        from pprint import pprint
        pprint(data)
    except Exception as e:
        print("Response is not JSON:", e)
except Exception as e:
    print("Request failed:", e)
