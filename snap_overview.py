import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page.goto("http://localhost:5173/")
        await page.wait_for_timeout(3000) # wait for data load
        await page.screenshot(path="overview_new.png")
        await browser.close()

asyncio.run(run())
