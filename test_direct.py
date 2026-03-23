import sys
from unittest.mock import MagicMock
import asyncio

sys.modules['aiohttp'] = MagicMock()
sys.modules['loguru'] = MagicMock()
sys.modules['PIL'] = MagicMock()

import db_manager as db_m
from db_manager import DBManager

db_m.db_manager = DBManager(':memory:')
db_m.db_manager.conn.execute("INSERT OR IGNORE INTO cookies (id, user_id) VALUES ('cookie1', 1)")
db_m.db_manager.conn.execute("INSERT INTO risk_control_logs (cookie_id, event_description) VALUES ('cookie1', 'test_log')")
db_m.db_manager.conn.commit()

from reply_server import get_admin_risk_control_logs

async def main():
    admin = {"user_id": 1, "username": "admin"}
    res = await get_admin_risk_control_logs(limit=100, offset=0, admin_user=admin)
    print("API Response:", res)

asyncio.run(main())
