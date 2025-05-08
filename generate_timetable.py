import sqlite3
from datetime import datetime, timedelta
import random

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
START_TIME = datetime.strptime("08:30", "%H:%M")
END_TIME = datetime.strptime("18:00", "%H:%M")
LUNCH_START = datetime.strptime("12:30", "%H:%M")
LUNCH_END = datetime.strptime("13:30", "%H:%M")
SLOT_DURATION = timedelta(minutes=60)

def get_time_slots():
    slots = []
    current = START_TIME
    while current + SLOT_DURATION <= END_TIME:
        if not (LUNCH_START <= current < LUNCH_END):
            end = current + SLOT_DURATION
            slots.append(f"{current.strftime('%H:%M')}-{end.strftime('%H:%M')}")
        current += SLOT_DURATION
    return slots

def auto_generate_timetable(branch, semester):
    conn = sqlite3.connect('timetable.db')
    cur = conn.cursor()

    # ✅ Do not regenerate if already exists
    cur.execute("SELECT COUNT(*) FROM timetable WHERE branch=? AND semester=?", (branch, semester))
    if cur.fetchone()[0] > 0:
        conn.close()
        return "already_exists"

    # Create timetable table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT,
            time_slot TEXT,
            subject TEXT,
            professor_name TEXT,
            branch TEXT,
            semester INTEGER
        )
    """)

    cur.execute("SELECT * FROM subjects WHERE branch=? AND semester=?", (branch, semester))
    subjects = cur.fetchall()
    random.shuffle(subjects)

    time_slots = get_time_slots()
    professor_schedule = {}
    day_slot_map = {day: [] for day in DAYS}
    day_index = 0

    for subject in subjects:
        _, sub_name, hours, prof_name, _, _ = subject
        is_lab = hours == 2
        assigned = 0
        attempts = 0

        while assigned < hours and attempts < 100:
            day = DAYS[day_index % len(DAYS)]
            used_slots = day_slot_map[day]

            for slot in time_slots:
                if is_lab:
                    i = time_slots.index(slot)
                    if i + 1 >= len(time_slots): continue
                    next_slot = time_slots[i + 1]

                    if (slot in used_slots or next_slot in used_slots): continue
                    if any((day, s) in professor_schedule.get(prof_name, []) for s in [slot, next_slot]): continue

                    cur.execute("""
                        INSERT INTO timetable (day, time_slot, subject, professor_name, branch, semester)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (day, slot, sub_name, prof_name, branch, semester))
                    cur.execute("""
                        INSERT INTO timetable (day, time_slot, subject, professor_name, branch, semester)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (day, next_slot, sub_name, prof_name, branch, semester))

                    used_slots.extend([slot, next_slot])
                    professor_schedule.setdefault(prof_name, []).extend([(day, slot), (day, next_slot)])
                    assigned = 2
                    break
                else:
                    if slot in used_slots: continue
                    if (day, slot) in professor_schedule.get(prof_name, []): continue

                    cur.execute("""
                        INSERT INTO timetable (day, time_slot, subject, professor_name, branch, semester)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (day, slot, sub_name, prof_name, branch, semester))

                    used_slots.append(slot)
                    professor_schedule.setdefault(prof_name, []).append((day, slot))
                    assigned += 1
                    break

            day_index += 1
            attempts += 1

    conn.commit()
    conn.close()
    return "generated"
