import sqlite3

db = r"C:\Users\singh\Videos\AthenaBenchmarkWorkspace\.athena\index.db"

conn = sqlite3.connect(db)

print(conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall())