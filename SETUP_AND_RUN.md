# ⚙️ SETUP & RUN GUIDE
## Student Attendance & Grade Management System (SAGMS)

---

## Prerequisites

| Tool | Minimum Version | Download |
|------|----------------|---------|
| Python | 3.10+ | https://python.org |
| PostgreSQL | 13+ | https://postgresql.org |
| pip | bundled with Python | — |

---

## Step 1 — Clone / Locate the Project

```
d:\V\2026\Project\Yoshita\
├── app.py               ← Flask application
├── db_config.py         ← Database connection helper
├── schema.sql           ← PostgreSQL schema (tables, trigger, views, indexes)
├── sample_data.sql      ← Pre-loaded demo data (10 students, 5 courses)
├── setup_db.py          ← One-shot DB initialisation script
├── audit.py             ← Full project health-check script
├── requirements.txt     ← Python dependencies
├── .env                 ← Environment variables (DB credentials)
├── static/
│   ├── style.css
│   └── main.js
└── templates/           ← 16 Jinja2 HTML templates
```

---

## Step 2 — Configure Environment

Open `.env` and set your PostgreSQL credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=attendance_db
DB_USER=postgres
DB_PASSWORD=your_actual_password_here
FLASK_SECRET_KEY=mysecretkey2026
```

> **Important:** Use the literal password — no URL-encoding.
> Example: if your password is `postgresql@123`, write it exactly as `postgresql@123`.

---

## Step 3 — Install Python Dependencies

Open a terminal in the project folder and run:

```powershell
pip install -r requirements.txt
```

This installs:
- `Flask 3.0.3` — Web framework
- `psycopg2-binary 2.9.9` — PostgreSQL driver
- `python-dotenv 1.0.1` — .env file loader
- `Werkzeug 3.0.3` — WSGI utilities

---

## Step 4 — Initialise the Database

Run the one-shot setup script. This will:
1. Create the `attendance_db` PostgreSQL database
2. Apply `schema.sql` (all tables, trigger, views, indexes)
3. Load `sample_data.sql` (demo records)

```powershell
python setup_db.py
```

Expected output:
```
=== SAGMS Database Setup ===
[OK] Database 'attendance_db' created.
[OK] schema.sql applied.
[OK] sample_data.sql applied.
Setup complete! Run: python app.py
```

> **If the database already exists**, the script skips creation and re-runs the schema.
> Re-running is safe — `DROP ... IF EXISTS` statements in `schema.sql` handle cleanup.

---

## Step 5 — Run the Application

```powershell
python app.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

---

## Step 6 — (Optional) Run the Audit

To verify every component of the project is working:

```powershell
python audit.py
```

A clean project reports:
```
RESULT: 60/60 checks passed
STATUS: ALL CLEAR - Project is complete!
```

---

## All Available Pages

| URL | Description |
|-----|-------------|
| `/` | Dashboard — stats, charts, alerts |
| `/students` | List all students |
| `/students/add` | Add a new student |
| `/students/edit/<id>` | Edit student details |
| `/courses` | List all courses |
| `/courses/add` | Add a new course |
| `/courses/edit/<id>` | Edit course details |
| `/enrollments` | Manage student–course enrollments |
| `/attendance` | View & filter attendance records |
| `/attendance/mark` | Mark attendance for a course |
| `/grades` | View & filter grade records |
| `/grades/entry` | Enter or update a student grade |
| `/reports` | Reports index |
| `/reports/attendance` | Attendance summary report |
| `/reports/grades` | Grade summary report |
| `/reports/top_students` | Top student rankings with podium |
| `/reports/low_attendance` | At-risk students alert |
| `/api/enrolled_students` | JSON API for AJAX attendance loading |

---

## Troubleshooting

### `password authentication failed for user "postgres"`
- Check your `.env` — the password must be the **literal** password, not URL-encoded.
- Verify PostgreSQL is running: `pg_ctl status` or check Windows Services.

### `ModuleNotFoundError: No module named 'flask'`
- Run `pip install -r requirements.txt` again.
- Ensure you are using the correct Python environment.

### `relation "students" does not exist`
- Run `python setup_db.py` to create tables.

### Port 5000 already in use
- Change the port in `app.py` last line: `app.run(debug=True, port=5001)`

### Cannot connect to PostgreSQL on Windows
- Start PostgreSQL: Search "Services" in Windows → Start `postgresql-x64-XX`.
- Or run: `net start postgresql-x64-16` (adjust version number).

---

## Stopping the Server

Press `Ctrl + C` in the terminal running `python app.py`.
