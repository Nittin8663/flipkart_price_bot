import asyncio
from playwright.async_api import async_playwright

async def get_croma_price(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # show browser
        page = await browser.new_page()
        print("Opening URL...")
        await page.goto(url, timeout=30000)
        print("Page loaded.")

        body = await page.inner_text("body")
        print("Body text length:", len(body))

        await browser.close()
        return "DONE"

if __name__ == "__main__":
    url = "https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011"
    result = asyncio.run(get_croma_price(url))
    print("Result:", result)
