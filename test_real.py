from fastapi.testclient import TestClient
import db_manager as db_m
from db_manager import DBManager

db_m.db_manager = DBManager(':memory:')
db_m.db_manager.conn.execute("CREATE TABLE IF NOT EXISTS cookies (id TEXT PRIMARY KEY, cookies_str TEXT, user_id INTEGER, enabled BOOLEAN DEFAULT 1, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
db_m.db_manager.conn.execute("INSERT OR IGNORE INTO cookies (id, cookies_str, user_id) VALUES ('cookie1', 'abc', 1)")
db_m.db_manager.conn.execute("""
CREATE TABLE IF NOT EXISTS risk_control_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cookie_id TEXT NOT NULL,
    event_type TEXT NOT NULL DEFAULT 'slider_captcha',
    event_description TEXT,
    processing_result TEXT,
    processing_status TEXT DEFAULT 'processing',
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cookie_id) REFERENCES cookies(id) ON DELETE CASCADE
)
""")
db_m.db_manager.conn.execute("INSERT INTO risk_control_logs (cookie_id, event_description) VALUES ('cookie1', 'test_log')")
db_m.db_manager.conn.commit()

from reply_server import app
from reply_server import require_admin
app.dependency_overrides[require_admin] = lambda: {"user_id": 1, "username": "admin"}

client = TestClient(app)
res = client.get("/admin/risk-control-logs?limit=100&offset=0")
print("Response JSON:")
print(res.json())
