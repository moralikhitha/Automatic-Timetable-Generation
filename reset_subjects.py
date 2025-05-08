import sqlite3

conn = sqlite3.connect("timetable.db")
cur = conn.cursor()

# Drop old table if exists
cur.execute("DROP TABLE IF EXISTS subjects")

# Create new table with professor_name as TEXT
cur.execute("""
CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    hours_per_week INTEGER,
    professor_name TEXT,
    branch TEXT,
    semester INTEGER
)
""")

conn.commit()
conn.close()
print("✅ Subjects table reset successfully!")
