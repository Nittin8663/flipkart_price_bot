import requests

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,hi;q=0.8,de;q=0.7',
    'anonymous_id': 'd46a37d0-c7e3-4db8-99c5-cbdad1c55428',
    'client_id': 'TCP-WEB-APP',
    'client_secret': '6fe27bd7-658d-4d28-ab66-a71da9637529',
    'content-type': 'application/json',
    'jarvissessionid': 'e392f5e4-9dae-4cf2-8f07-9d2f04d72a6a',
    'neu-app-version': '6.1.0',
    'origin': 'https://www.tataneu.com',
    'priority': 'u=1, i',
    'programid': '01eae2ec-0576-1000-bbea-86e16dcb4b79',
    'referer': 'https://www.tataneu.com/',
    'request_id': '005ad92b-57d1-4ac2-96bf-0229ebdb2197',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'x-offer-benefit-threshold': '50',
}

params = {
    'skuId': '312576',
    'category': 'electronics',
    'pinCode': '400001',
    'categoryId': '10',
}

cookies = {
    "ak_bmsc": "A2D964DD9282DF1701072ACC1775F2A6~000000000000000000000000000000~YAAQVnBWuMl3pbeYAQAAvFekxhzjcgp1N+X4VG/F5/VrzTkADzYil/8Tgi+D6BvQ/JT5N32AyUP/oqwRrm998i9QvGgKYwtE751OdY2SUGFNAS1Jf4lxKFsQub0FFKCjP/sYRie2ocG2r+Qkcdm3V09ufIluTFNkeg0Hzx1A9gF7nca1nzxFdyyz9bAK1F+Qxcu9UA/W/if+84e24uoAaGZOKkamRWHr80UkuXR1+Lx6u4z87Rpkb32lABuAzOGRqHqKkrNxPV/9zglJLn87dgMqBH+ZhRliPHrbg4nwKihXVmJwU2AuGaZqDuJiaDfd/B7eAWC8FFIcC8DcpOsNt4Jj8b9FO8D3ty4LXY3AxdrMX4HQg8gyFSg75SaD52I9l4LTa0Yri/4D0jNcpcxvgL1OH5KJ5/2/AsmuCVZ9wr/7AMkQ6PBs38Veuw==",
    "bm_sz": "3602150F8D7C2DBE9B56D5FB4A982CE6~YAAQVnBWuBe6q7eYAQAA7m2yxhzMrgQ69pjetrILDSosww84eNdGNymL5momC+ui8o8+JTsZAjOXuK8jxNvcgqAA9/wBqudRArBQu+/WccdrJ3zUMnsZCmpVMDVVlOj3hRnlZPCKa5r7VBqMPsI641MPxJgf03YBypeCEIfW0F6gCjSrZ3qGfeDxj51XnNEaDk96bRhmvc23i+HAfhD4bArXX4jtlCgi2INRohKiG67/tgJOTeG5drMVLoEm8mfiXRCOcrtxta/EvU2G9S9jGpKbvvihyJ9ocELHQ+1PUtYzkF5hyqVDbb/FDaUV0SfIdwkHWJH141xPq3kECo1/LWJI7PCHKOlbNtTyW4caoMV1fhtYaN/FQgElbTxMiVEZj7RQ9/pIglJA6EydMEgwfjSFD3ogGHEu0DOVwI1MabYHJrAf0Yyhg7yPB5vHFzh3LNM1q/l9nKRA8EcPw03FdWcsmj39sBZ0jKY=~3163458~3753281"
}

response = requests.get(
    'https://api.tatadigital.com/api/v2/commerce/product-offers',
    params=params,
    headers=headers,
    cookies=cookies
)

print("Status code:", response.status_code)
print("Raw response:", response.text)

try:
    data = response.json()
    print("Parsed JSON:")
    print(data)
except Exception as e:
    print("Response is not JSON:", e)
