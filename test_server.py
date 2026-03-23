import sys
from unittest.mock import MagicMock
sys.modules['aiohttp'] = MagicMock()
sys.modules['loguru'] = MagicMock()
sys.modules['PIL'] = MagicMock()

import db_manager as db_m
from db_manager import DBManager

db_m.db_manager = DBManager('test_db_3.db')
db_m.db_manager.conn.execute("INSERT OR IGNORE INTO cookies (id, user_id) VALUES ('cookie1', 1)")
db_m.db_manager.conn.execute("INSERT INTO risk_control_logs (cookie_id, event_description) VALUES ('cookie1', 'test_log')")
db_m.db_manager.conn.commit()

import uvicorn
import threading
from reply_server import app
from reply_server import require_admin
import time
import json
import urllib.request
from urllib.error import HTTPError

app.dependency_overrides[require_admin] = lambda: {"user_id": 1, "username": "admin"}

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8002, log_level="error")

t = threading.Thread(target=run_server, daemon=True)
t.start()

time.sleep(2)
try:
    req = urllib.request.Request("http://127.0.0.1:8002/admin/risk-control-logs?limit=100&offset=0")
    with urllib.request.urlopen(req) as res:
        print("STATUS:", res.status)
        data = res.read().decode('utf-8')
        print("JSON:", json.loads(data))
except HTTPError as e:
    print("HTTPError:", e.code)
    print("BODY:", e.read().decode('utf-8'))
except Exception as e:
    print("ERROR:", e)
