import sys
from unittest.mock import MagicMock
sys.modules['fastapi'] = MagicMock()
sys.modules['fastapi.staticfiles'] = MagicMock()
sys.modules['fastapi.responses'] = MagicMock()
sys.modules['fastapi.security'] = MagicMock()
sys.modules['pydantic'] = MagicMock()
sys.modules['uvicorn'] = MagicMock()
sys.modules['loguru'] = MagicMock()

import db_manager as db_m
from db_manager import DBManager

db_m.db_manager = DBManager(':memory:')
db_m.db_manager.conn.execute("INSERT OR IGNORE INTO cookies (id, user_id) VALUES ('cookie1', 1)")
db_m.db_manager.conn.execute("INSERT INTO risk_control_logs (cookie_id, event_description) VALUES ('cookie1', 'test_log')")
db_m.db_manager.conn.commit()

import reply_server
import asyncio

async def main():
    admin = {"user_id": 1, "username": "admin"}
    res = await reply_server.get_admin_risk_control_logs(limit=100, offset=0, admin_user=admin)
    print("API Response:", res)

asyncio.run(main())
