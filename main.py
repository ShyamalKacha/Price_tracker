import os
import asyncio
import requests
from playwright.async_api import async_playwright

# Telegram bot credentials
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Function to send Telegram notification
def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
        print("Notification sent!")
    except Exception as e:
        print("Failed to send Telegram message:", e)

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = page = await browser.new_page(viewport={"width": 1280, "height": 800},user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36")
        await page.goto("https://www.flipkart.com/cmf-nothing-phone-2-pro-black-128-gb/p/itm46a119f176627?pid=MOBHAUHA5GRW9FS2&lid=LSTMOBHAUHA5GRW9FS2TVI8FR&marketplace=FLIPKART&q=cmf%20phone%202&sattr[]=color&sattr[]=storage&st=color")

        # Extract price
        element = await page.query_selector('div.Nx9bqj.CxhGGd')
        price = int((await element.inner_text()).replace("₹", "").replace(",", ""))
        print("Price:", price)

        # Condition for alert
        if price < 19999:
            send_telegram_message(f"📢 Price Drop Alert!\nCMF Phone 2 Pro is now ₹{price}")

        await browser.close()

asyncio.run(run())
