import os
import asyncio
import requests
from playwright.async_api import async_playwright

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SCRAPERAPI_KEY = os.getenv("SCRAPERAPI_KEY")


def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

async def run():
    target_url = "https://www.flipkart.com/cmf-nothing-phone-2-pro-black-128-gb/p/itm46a119f176627"

    # Wrap target URL with ScraperAPI
    scraper_url = f"http://api.scraperapi.com?api_key={SCRAPERAPI_KEY}&country_code=in&url={target_url}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )

        response=await page.goto(scraper_url, wait_until="networkidle")
        # print("Region:", response.headers.get("scraper-region"))

        # Wait until the price element loads
        element = await page.wait_for_selector('div.Nx9bqj.CxhGGd', timeout=30000)
        price_text = await element.inner_text()
        price = int(price_text.replace("₹", "").replace(",", ""))
        # print("Price:", price)  

        if price < 19999:
            send_telegram_message(f"📢 Price Drop Alert!\nCMF Phone 2 Pro is now ₹{price}")
        
        # target_url="https://ipinfo.io/json"
        # scraper_url = f"http://api.scraperapi.com?api_key={SCRAPERAPI_KEY}&country_code=in&url={target_url}"

        # await page.goto(scraper_url, wait_until="networkidle")
        # print(await page.inner_text("pre"))

        await browser.close()

asyncio.run(run())
