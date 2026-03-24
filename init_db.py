import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE donors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    blood TEXT,
    city TEXT,
    phone TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully!")