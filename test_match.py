import sqlite3
import os

db_path = 'data/xianyu_data.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT keyword, hex(keyword) FROM delivery_rules WHERE keyword LIKE '%趣学Python算法100例%'")
res = cursor.fetchone()
print(f"Keyword: {res[0]}")
print(f"Hex: {res[1]}")

search_text = "《趣学Python算法100例》是电子版【PDF】哦，随时随"
print(f"Search Text: {search_text}")

# Test matching in Python
if res[0] in search_text:
    print("Python match: YES")
else:
    print("Python match: NO")

# Test matching in SQLite
cursor.execute("SELECT ? LIKE '%' || keyword || '%' FROM delivery_rules WHERE keyword LIKE '%趣学Python算法100例%'", (search_text,))
print(f"SQLite match: {cursor.fetchone()[0]}")

conn.close()
