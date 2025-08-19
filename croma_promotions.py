import requests

url = "https://api.tatadigital.com/api/v1/commerce/benefit-offers?skuId=312576&category=electronics&pinCode=400001&categoryId=10"

headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "anonymous_id": "8cd4bc58-0c0c-48e0-a19b-661e1cba7fb6",
    "client_id": "TCP-WEB-APP",
    "client_secret": "6fe27bd7-658d-4d28-ab66-a71da9637529",
    "content-type": "application/json",
    "jarvissessionid": "c4ecacb8-dbaf-4548-a80e-5678503b5abb",
    "neu-app-version": "6.1.0",
    "origin": "https://www.tataneu.com",
    "priority": "u=1, i",
    "programid": "01eae2ec-0576-1000-bbea-86e16dcb4b79",
    "referer": "https://www.tataneu.com/",
    "request_id": "01c1850f-78c5-4baa-9b23-2bbe77d15dae",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "x-offer-benefit-threshold": "50"
}

response = requests.get(url, headers=headers)
print("Status Code:", response.status_code)
print("Response:")
print(response.text)
