import asyncio
from playwright.async_api import async_playwright

async def fetch_page(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()
        await browser.close()
        return content

# Example usage
if __name__ == "__main__":
    url = "http://13.48.13.46/"
    html = asyncio.run(fetch_page(url))
    print(html[:500])  # Print first 500 chars