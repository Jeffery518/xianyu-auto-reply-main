import sqlite3
import os

db_path = 'data/xianyu_data.db'
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("--- Delivery Rules ---")
cursor.execute("SELECT keyword, card_id, enabled FROM delivery_rules")
rules = cursor.fetchall()
for r in rules:
    print(r)

print("\n--- Cards ---")
cursor.execute("SELECT id, name, type, text_content FROM cards")
cards = cursor.fetchall()
for c in cards:
    print(c)

conn.close()
