import sys
from unittest.mock import MagicMock
import asyncio

sys.modules['fastapi'] = MagicMock()
sys.modules['fastapi.staticfiles'] = MagicMock()
sys.modules['fastapi.responses'] = MagicMock()
sys.modules['fastapi.security'] = MagicMock()
sys.modules['pydantic'] = MagicMock()
sys.modules['uvicorn'] = MagicMock()
sys.modules['loguru'] = MagicMock()
sys.modules['aiohttp'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['requests'] = MagicMock()
sys.modules['openpyxl'] = MagicMock()
sys.modules['openai'] = MagicMock()
sys.modules['playwright'] = MagicMock()
sys.modules['playwright.sync_api'] = MagicMock()
sys.modules['playwright.async_api'] = MagicMock()

import db_manager as db_m
from db_manager import DBManager

db_m.db_manager = DBManager(':memory:')
db_m.db_manager.conn.execute("INSERT OR IGNORE INTO cookies (id, user_id) VALUES ('cookie1', 1)")
db_m.db_manager.conn.execute("INSERT INTO risk_control_logs (cookie_id, event_description) VALUES ('cookie1', 'test_log')")
db_m.db_manager.conn.commit()

import reply_server

async def main():
    admin = {"user_id": 1, "username": "admin"}
    res = await reply_server.get_admin_risk_control_logs(cookie_id=None, status=None, limit=100, offset=0, admin_user=admin)
    print("API Response:")
    print(res)

asyncio.run(main())
