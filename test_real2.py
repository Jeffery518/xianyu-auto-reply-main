from fastapi.testclient import TestClient
import db_manager as db_m
from db_manager import DBManager

db_m.db_manager = DBManager(':memory:')
db_m.db_manager.conn.execute("INSERT OR IGNORE INTO cookies (id, user_id) VALUES ('cookie1', 1)")
db_m.db_manager.conn.execute("INSERT INTO risk_control_logs (cookie_id, event_description) VALUES ('cookie1', 'test_log')")
db_m.db_manager.conn.commit()

from reply_server import app
from reply_server import require_admin
app.dependency_overrides[require_admin] = lambda: {"user_id": 1, "username": "admin"}

client = TestClient(app)
res = client.get("/admin/risk-control-logs?limit=100&offset=0")
print("Response JSON:")
print(res.json())
