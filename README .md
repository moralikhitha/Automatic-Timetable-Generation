
# Timetable Generation Web Application

A web utility designed to simplify and automate timetable creation for academic institutions. The system supports role-based access for Admins, Faculty, and Students, allowing seamless schedule management.

##  Features

- **Admin Panel**
  - Generate and update class timetables
  - Assign faculty and subjects to classes
  - Modify student and faculty information
- **Faculty Portal**
  - View personal timetable
- **Student Portal**
  - View class timetable
- **Conflict Handling**
  - Detects and allows manual resolution of timetable conflicts
- **Future Scope**
  - API integration
  - Mobile app interface
  - Real-time notifications for updates

## Team

- **Project Manager**: Joshika  
- **Frontend Developers**: Bhargavi, Rashmitha  
- **Backend Developers**: Likhitha, Rishika  

## Project Duration

February 2025 – May 2025

##  Tech Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap  
- **Backend**: Python (Flask or Django)  
- **Database**: MySQL / SQLite  

## 📂 Project Structure

```bash
timetable-generator/
├── frontend/
│   ├── index.html
│   ├── view_timetable.html
│   └── admin_panel.html
├── backend/
│   ├── app.py
│   ├── routes/
│   └── models/
├── static/
│   ├── css/
│   └── js/
├── templates/
│   └── *.html
├── README.md
└── requirements.txt
```

##  How to Run the Project

1. **Clone the repository** (or download the source files):

   ```bash
   git clone https://github.com/your-repo/timetable-generator.git
   cd timetable-generator
   ```

2. **Install required Python packages**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:

   ```bash
   python app.py
   ```

4. **Open your browser** and go to the following link that appears in the terminal. For example:

   ```
   http://127.0.0.1:5000/
   ```

5. **To log in**, type `/login` at the end of the URL:

   ```
   http://127.0.0.1:5000/login
   ```

6. **Login Credentials**:
   - **Admin Username**: admin  
   - **Password**: admin123  

   Once logged in, you'll be directed to the admin panel, where you can generate timetables, assign faculty, and more.

##  License

This project is intended for academic use only.
