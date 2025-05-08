from flask import Flask, render_template, request, jsonify, redirect
import sqlite3
from utils.generate_timetable import auto_generate_timetable

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('timetable.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return "Welcome to Smart Timetable System"

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/save_subjects', methods=['POST'])
def save_subjects():
    data = request.json
    branch = data['branch']
    semester = data['semester']
    subjects = data['subjects']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM subjects WHERE branch=? AND semester=?", (branch, semester))

    for sub in subjects:
        cur.execute(
            "INSERT INTO subjects (name, hours_per_week, professor_name, branch, semester) VALUES (?, ?, ?, ?, ?)",
            (sub['name'], sub['hours'], sub['professor_name'], branch, semester)
        )

    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/get_subjects', methods=['GET'])
def get_subjects():
    branch = request.args.get('branch')
    semester = request.args.get('semester')

    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM subjects WHERE branch=? AND semester=?", (branch, semester)).fetchall()
    conn.close()
    return jsonify({'subjects': [dict(row) for row in rows]})

@app.route('/generate_timetable', methods=['POST'])
def generate_timetable():
    data = request.json
    branch = data['branch']
    semester = data['semester']
    status = auto_generate_timetable(branch, semester)
    return jsonify({'status': status})


@app.route('/view_timetable')
def view_timetable():
    branch = request.args.get('branch', 'CSE')
    semester = request.args.get('semester', '2')

    print("🔍 Viewing timetable for:", branch, semester)

    conn = get_db_connection()
    rows = conn.execute("""
        SELECT day, time_slot, subject, professor_name
        FROM timetable
        WHERE branch=? AND semester=?
    """, (branch, semester)).fetchall()
    conn.close()

    print("✅ Found", len(rows), "rows")

    return render_template('view_timetable.html', rows=rows, branch=branch, semester=semester)

@app.route('/faculty')
def faculty_login():
    return render_template('faculty.html')

@app.route('/faculty_timetable')
def faculty_timetable():
    prof_name = request.args.get('name')
    branch = request.args.get('branch')
    semester = request.args.get('semester')

    conn = get_db_connection()
    rows = conn.execute("""
        SELECT day, time_slot, subject, professor_name
        FROM timetable
        WHERE LOWER(TRIM(professor_name)) = LOWER(TRIM(?))
        AND branch = ? AND semester = ?
        ORDER BY 
            CASE day 
                WHEN 'Monday' THEN 1
                WHEN 'Tuesday' THEN 2
                WHEN 'Wednesday' THEN 3
                WHEN 'Thursday' THEN 4
                WHEN 'Friday' THEN 5
            END, time_slot
    """, (prof_name, branch, semester)).fetchall()
    conn.close()

    return render_template('faculty_timetable.html', rows=rows, prof_name=prof_name, branch=branch, semester=semester)
@app.route('/reset_timetable', methods=['POST'])
def reset_timetable():
    data = request.json
    branch = data['branch']
    semester = data['semester']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM timetable WHERE branch=? AND semester=?", (branch, semester))
    conn.commit()
    conn.close()

    return jsonify({'status': 'reset'})
@app.route('/student')
def student_login():
    return render_template('student.html')

@app.route('/student_timetable')
def student_timetable():
    branch = request.args.get('branch')
    semester = request.args.get('semester')

    conn = get_db_connection()
    rows = conn.execute("""
        SELECT day, time_slot, subject, professor_name
        FROM timetable
        WHERE branch = ? AND semester = ?
        ORDER BY 
            CASE day 
                WHEN 'Monday' THEN 1
                WHEN 'Tuesday' THEN 2
                WHEN 'Wednesday' THEN 3
                WHEN 'Thursday' THEN 4
                WHEN 'Friday' THEN 5
            END, time_slot
    """, (branch, semester)).fetchall()
    conn.close()

    return render_template('student_timetable.html', rows=rows, branch=branch, semester=semester)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    role = request.form.get('role')

    if role == 'admin':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            return redirect('/admin')
        else:
            return "❌ Invalid Admin Credentials"

    if role == 'faculty':
        name = request.form.get('name')
        branch = request.form.get('branch')
        semester = request.form.get('semester')
        return redirect(f"/faculty_timetable?name={name}&branch={branch}&semester={semester}")

    if role == 'student':
        branch = request.form.get('branch')
        semester = request.form.get('semester')
        return redirect(f"/student_timetable?branch={branch}&semester={semester}")

    return "❌ Invalid Role Selected"

@app.route('/logout')
def logout():
    # For now, just redirect to login page
    return redirect('/login')

if __name__ == '__main__':
    print("🚀 Flask app is running at http://127.0.0.1:5000")
    app.run(debug=True)
