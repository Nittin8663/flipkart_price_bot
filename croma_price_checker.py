import asyncio
from playwright.async_api import async_playwright

async def get_croma_price(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Product page open karo
        await page.goto(url, wait_until="domcontentloaded")

        # Croma me price ke liye common selectors
        selectors = [
            "span.amount",                  # Example: ₹19,999
            "span.pdp-price",               # Some product pages
            "span[data-testid='price']"     # Backup
        ]

        price = None
        for sel in selectors:
            try:
                element = page.locator(sel).first
                if await element.count() > 0:
                    text = await element.text_content()
                    if text and "₹" in text:
                        price = text.strip()
                        break
            except:
                continue

        await browser.close()
        return price or "PRICE NOT FOUND"

if __name__ == "__main__":
    url = "https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011"
    price = asyncio.run(get_croma_price(url))
    print("Croma Price:", price)
