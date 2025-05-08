import sqlite3

conn = sqlite3.connect("timetable.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS timetable")

cur.execute("""
CREATE TABLE timetable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT,
    time_slot TEXT,
    subject TEXT,
    professor_name TEXT,
    branch TEXT,
    semester INTEGER
)
""")

conn.commit()
conn.close()
print("✅ timetable table reset successfully!")
