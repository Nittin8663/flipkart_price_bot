from playwright.sync_api import sync_playwright

proxy = {
    "server": "http://gw.dataimpulse.com:10000",
    "username": "1258bd9e03f80533eb38__cr.in",
    "password": "ca69cf1263c65d0e",
}

with sync_playwright() as p:
    browser = p.chromium.launch(proxy=proxy, headless=False)
    page = browser.new_page()
    page.goto("https://www.croma.com/")
    print(page.title())
    browser.close()
