import sys
from unittest.mock import MagicMock
sys.modules['aiohttp'] = MagicMock()
sys.modules['loguru'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()

from db_manager import db_manager

def test_get_logs():
    with db_manager.lock:
        cursor = db_manager.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS risk_control_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cookie_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                event_description TEXT,
                processing_status TEXT DEFAULT 'processing',
                processing_result TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("INSERT INTO risk_control_logs (cookie_id, event_type, event_description) VALUES (?, ?, ?)", ("test", "slider", "test log"))
        db_manager.conn.commit()

    import json
    logs = db_manager.get_risk_control_logs(limit=5, offset=0)
    print(json.dumps(logs, indent=2))

if __name__ == "__main__":
    test_get_logs()
