import sqlite3

conn = sqlite3.connect("timetable.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS professors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    hours_per_week INTEGER,
    professor_id INTEGER,
    branch TEXT,
    semester INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS timetable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT,
    time_slot TEXT,
    subject_id INTEGER,
    professor_id INTEGER,
    branch TEXT,
    semester INTEGER
)
""")

conn.commit()
conn.close()
