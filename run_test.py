from unittest.mock import MagicMock
import sys
sys.modules['aiohttp'] = MagicMock()
sys.modules['loguru'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()

import asyncio
from playwright.async_api import async_playwright
import threading
import uvicorn
from reply_server import app

def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="critical")

async def main():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    await asyncio.sleep(2)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        page.on("console", lambda msg: print(f"Browser console [{msg.type}]: {msg.text}"))
        page.on("pageerror", lambda err: print(f"Browser page error: {err}"))

        await page.goto("http://127.0.0.1:8080/")
        await page.evaluate("localStorage.setItem('auth_token', 'mock_token');")
        await page.goto("http://127.0.0.1:8080/admin")
        await asyncio.sleep(1)

        print("Clicking risk control logs...")
        await page.evaluate("showSection('risk-control-logs')")
        await asyncio.sleep(2)

        html = await page.evaluate("document.getElementById('riskLogTableBody').innerHTML")
        print("Table innerHTML:")
        print(html)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
