import sys
from unittest.mock import MagicMock
import asyncio
from playwright.async_api import async_playwright
import threading
import uvicorn
import time

def start_server():
    from reply_server import app
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="critical")

async def main():
    from db_manager import db_manager
    # ensure dummy data
    with db_manager.lock:
        cursor = db_manager.conn.cursor()
        cursor.execute("INSERT INTO risk_control_logs (cookie_id, event_type, event_description) VALUES (?, ?, ?)", ("test_cookie", "slider", "test log"))

        # also we need a user to pass require_admin
        try:
            cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", ("admin", "admin@localhost", "hash"))
        except:
            pass # ignore if exists
        db_manager.conn.commit()

    # The mock_token needs to exist in SESSION_TOKENS
    from reply_server import SESSION_TOKENS
    SESSION_TOKENS['mock_token'] = {'user_id': 1, 'username': 'admin', 'timestamp': time.time()}

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
        await page.evaluate("""
            localStorage.setItem('auth_token', 'mock_token');
        """)
        # By bypassing verify, wait until JS is fully parsed
        await page.goto("http://127.0.0.1:8080/admin", wait_until='networkidle')
        await asyncio.sleep(2)

        print("Clicking risk control logs...")
        await page.evaluate("if (typeof showSection !== 'undefined') showSection('risk-control-logs')")

        # Wait a bit longer than 5 seconds to let the interval run
        print("Waiting 6 seconds...")
        await asyncio.sleep(6)

        display_style = await page.evaluate("document.getElementById('riskLogContainer').style.display")
        print(f"Container display style: {display_style}")

        html = await page.evaluate("document.getElementById('riskLogTableBody').innerHTML")
        print("Table rows present? ", "test_cookie" in html)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
