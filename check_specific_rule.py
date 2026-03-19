import sqlite3
import os

db_path = 'data/xianyu_data.db'
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("--- Rules for 趣学Python算法100例 ---")
cursor.execute("SELECT dr.keyword, c.name, c.is_multi_spec, c.enabled, dr.enabled FROM delivery_rules dr JOIN cards c ON dr.card_id = c.id WHERE dr.keyword LIKE '%趣学Python算法100例%'")
rules = cursor.fetchall()
for r in rules:
    print(r)

conn.close()
