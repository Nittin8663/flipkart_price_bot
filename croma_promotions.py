import requests

url = "https://www.croma.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

try:
    r = requests.get(url, headers=headers, timeout=15)
    print("Status code:", r.status_code)
    print("First 200 chars of response:\n", r.text[:200])
    if "Access Denied" in r.text or "blocked" in r.text.lower():
        print("⚠️ IP possibly blocked or bot detected!")
    else:
        print("✅ IP not blocked, content looks normal.")
except Exception as e:
    print("Error:", e)
