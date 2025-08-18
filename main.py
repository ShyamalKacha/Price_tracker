import os
import asyncio
import requests
from playwright.async_api import async_playwright

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.flipkart.com/cmf-nothing-phone-2-pro-black-128-gb/p/itm46a119f176627?pid=MOBHAUHA5GRW9FS2")

        element = await page.wait_for_selector('div.Nx9bqj.CxhGGd')
        price = int((await element.inner_text()).replace("₹", "").replace(",", ""))
        print("Price:", price)

        if price < 19999:
            send_telegram_message(f"📢 Price Drop Alert!\nCMF Phone 2 Pro is now ₹{price}")

        await browser.close()

asyncio.run(run())
