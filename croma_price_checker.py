import asyncio, re
from playwright.async_api import async_playwright

PRICE_RE = re.compile(r"(₹\s?\d[\d,]*)")

async def get_croma_price(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(url, wait_until="domcontentloaded", timeout=30000)

        selectors = [
            "span.amount",
            "span.pdp-price",
            "span[data-testid='price']"
        ]

        price = None
        for sel in selectors:
            try:
                element = page.locator(sel)
                if await element.count() > 0:
                    text = await element.first.text_content()
                    if text and "₹" in text:
                        price = text.strip()
                        break
            except Exception as e:
                print("Selector error:", e)

        # Fallback: regex on whole page
        if not price:
            body = await page.inner_text("body")
            m = PRICE_RE.search(body)
            if m:
                price = m.group(1)

        await browser.close()
        return price or "PRICE NOT FOUND"

if __name__ == "__main__":
    url = "https://www.croma.com/vivo-y19-5g-4gb-ram-128gb-titanium-silver-/p/315011"
    price = asyncio.run(get_croma_price(url))
    print("Croma Price:", price)
