from playwright.sync_api import sync_playwright

proxy = {
    "server": "http://74.81.81.81:823",
    "username": "1258bd9e03f80533eb38__cr.in",
    "password": "ca69cf1263c65d0e",
}

with sync_playwright() as p:
    browser = p.chromium.launch(proxy=proxy, headless=true)  # headless=False for human-like
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
        locale="en-US"
    )
    page = context.new_page()
    page.goto("https://www.croma.com/", timeout=60000)
    page.wait_for_timeout(5000)  # Wait for JS rendering
    print(page.title())
    browser.close()
