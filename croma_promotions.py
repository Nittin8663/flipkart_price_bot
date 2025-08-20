import requests

# Step 1: Get cookies from response
session = requests.Session()
response = session.get('https://api.tatadigital.com/api/v2/commerce/product-offers?skuId=312576&category=electronics&pinCode=400001&categoryId=10')
print(response.cookies)  # Show cookies received from response
