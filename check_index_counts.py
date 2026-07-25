import sqlite3

db = r"C:\Users\singh\Videos\AthenaBenchmarkWorkspace\.athena\index.db"

conn = sqlite3.connect(db)

for table in ["documents", "chunks"]:
    count = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(f"{table}: {count}")