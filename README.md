# Student Attendance & Grade Management System
### SAGMS — Final-Year DBMS Academic Project | Session 2025–26

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Core Objectives](#core-objectives)
3. [Technology Stack](#technology-stack)
4. [Database Concepts Demonstrated](#database-concepts-demonstrated)
5. [System Architecture](#system-architecture)
6. [Database Schema (ERD)](#database-schema-erd)
7. [Normalization Analysis](#normalization-analysis)
8. [Trigger — Auto Grade Calculation](#trigger--auto-grade-calculation)
9. [Views](#views)
10. [Indexes & Performance](#indexes--performance)
11. [Backend — Flask Application](#backend--flask-application)
12. [Frontend — UI Design](#frontend--ui-design)
13. [Features Walkthrough](#features-walkthrough)
14. [API Endpoint](#api-endpoint)
15. [Project File Structure](#project-file-structure)
16. [Sample Data](#sample-data)
17. [Audit Results](#audit-results)

---

## Project Overview

**SAGMS** (Student Attendance & Grade Management System) is a fully functional, full-stack web application built as a Final-Year Database Management Systems (DBMS) project. It provides a faculty-facing portal to manage students, courses, enrollments, attendance, and grades — all backed by a normalized PostgreSQL database with advanced features including stored triggers, materialized views, and composite indexes.

The system demonstrates end-to-end application of relational database theory — from schema normalization to SQL aggregation — integrated with a clean Flask backend and a professional dark-themed UI.

---

## Core Objectives

| # | Objective | Status |
|---|-----------|--------|
| 1 | Design a 3NF-normalized relational schema | Done |
| 2 | Implement PostgreSQL triggers for auto-computation | Done |
| 3 | Create database views for aggregate reporting | Done |
| 4 | Apply indexes for query performance optimization | Done |
| 5 | Build full CRUD operations for all entities | Done |
| 6 | Demonstrate complex JOIN queries across 5 tables | Done |
| 7 | Generate analytics and exception reports | Done |
| 8 | Build a responsive, modern Faculty Portal UI | Done |

---

## Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Database** | PostgreSQL | 13+ | Primary RDBMS |
| **ORM/Driver** | psycopg2-binary | 2.9.9 | Raw SQL via Python |
| **Backend** | Flask | 3.0.3 | Web framework + routing |
| **Templating** | Jinja2 | 3.1.x | Server-side HTML rendering |
| **Environment** | python-dotenv | 1.0.1 | .env config management |
| **WSGI** | Werkzeug | 3.0.3 | HTTP request/response |
| **Frontend CSS** | Vanilla CSS | — | Custom dark-mode design |
| **Frontend JS** | Vanilla JS | ES6+ | AJAX, counters, animations |
| **Icons** | Bootstrap Icons | 1.11.3 | CDN icon library |
| **Fonts** | Google Fonts | — | Inter + Outfit typefaces |

> **Design choice:** Raw SQL (`psycopg2`) was used **instead of an ORM** (like SQLAlchemy) deliberately — this showcases direct SQL skills relevant to a DBMS project, including JOINs, subqueries, UPSERT, and GROUP BY.

---

## Database Concepts Demonstrated

### 1. Relational Integrity
- Every foreign key enforces `ON DELETE CASCADE` — deleting a student automatically removes their attendance and grade records.
- `UNIQUE` constraints prevent duplicate enrollments (`student_id, course_id`) and duplicate attendance records (`student_id, course_id, date`).
- `CHECK` constraints enforce data validity: grade marks bounded to `[0, 50]`, attendance status restricted to `('Present', 'Absent', 'Late')`, and credits must be `> 0`.

### 2. Normalization (3NF)
See detailed analysis below.

### 3. Stored Trigger
An automatic trigger computes `total_marks` and assigns a letter `grade` on every INSERT or UPDATE to the `grades` table — no application-level computation needed.

### 4. Views (Virtual Tables)
Two views encapsulate complex multi-table aggregation logic, acting as reusable query interfaces.

### 5. Composite Indexes
Seven B-tree indexes accelerate attendance and grade lookups by student, course, and date.

### 6. UPSERT (INSERT ... ON CONFLICT)
The mark-attendance and grade-entry operations use PostgreSQL's `ON CONFLICT ... DO UPDATE` to safely handle re-submissions without duplicates.

### 7. Aggregate Queries
Dashboard and reports use `COUNT`, `SUM`, `AVG`, `MAX`, `MIN`, `ROUND`, `NULLIF`, `COALESCE`, and `CASE` expressions across joined tables.

### 8. Subqueries & CTEs
Reports use correlated subqueries to compute attendance percentage and rank students.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Browser (Client)                    │
│         HTML + CSS + Vanilla JS (Bootstrap Icons)        │
└─────────────────────┬───────────────────────────────────┘
                      │  HTTP Request / Response
┌─────────────────────▼───────────────────────────────────┐
│                   Flask Web Server                       │
│                     app.py                              │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Route Handlers (25 endpoints)                   │   │
│  │  GET/POST → query_db() / execute_db()            │   │
│  │  Jinja2 template rendering                       │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────┘
                      │  psycopg2 (raw SQL)
┌─────────────────────▼───────────────────────────────────┐
│                  PostgreSQL Database                     │
│                   attendance_db                         │
│                                                         │
│   ┌──────────┐  ┌─────────┐  ┌─────────────┐           │
│   │ students │  │ courses │  │ enrollments │           │
│   └────┬─────┘  └────┬────┘  └──────┬──────┘           │
│        │             │              │                   │
│   ┌────▼─────────────▼──────┐  ┌───▼──────┐            │
│   │      attendance         │  │  grades  │            │
│   └─────────────────────────┘  └────┬─────┘            │
│                                     │                   │
│   ┌──────────────────┐  ┌───────────▼──────────────┐   │
│   │ v_att_summary    │  │    trg_calculate_grade   │   │
│   │ v_grade_summary  │  │   (BEFORE INSERT/UPDATE) │   │
│   └──────────────────┘  └──────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## Database Schema (ERD)

### Tables

#### `students`
| Column | Type | Constraints |
|--------|------|-------------|
| `student_id` | SERIAL | PRIMARY KEY |
| `name` | VARCHAR(100) | NOT NULL |
| `email` | VARCHAR(150) | NOT NULL, UNIQUE |
| `department` | VARCHAR(100) | NOT NULL |
| `phone` | VARCHAR(15) | nullable |
| `created_at` | TIMESTAMP | DEFAULT NOW() |

#### `courses`
| Column | Type | Constraints |
|--------|------|-------------|
| `course_id` | SERIAL | PRIMARY KEY |
| `course_name` | VARCHAR(150) | NOT NULL |
| `course_code` | VARCHAR(20) | NOT NULL, UNIQUE |
| `credits` | INTEGER | NOT NULL, CHECK > 0 |
| `department` | VARCHAR(100) | nullable |
| `created_at` | TIMESTAMP | DEFAULT NOW() |

#### `enrollments` *(junction table)*
| Column | Type | Constraints |
|--------|------|-------------|
| `enrollment_id` | SERIAL | PRIMARY KEY |
| `student_id` | INTEGER | FK → students, CASCADE |
| `course_id` | INTEGER | FK → courses, CASCADE |
| `enrolled_on` | DATE | DEFAULT CURRENT_DATE |
| — | — | UNIQUE(student_id, course_id) |

#### `attendance`
| Column | Type | Constraints |
|--------|------|-------------|
| `attendance_id` | SERIAL | PRIMARY KEY |
| `student_id` | INTEGER | FK → students, CASCADE |
| `course_id` | INTEGER | FK → courses, CASCADE |
| `date` | DATE | NOT NULL |
| `status` | VARCHAR(10) | CHECK IN ('Present','Absent','Late') |
| — | — | UNIQUE(student_id, course_id, date) |

#### `grades`
| Column | Type | Constraints |
|--------|------|-------------|
| `grade_id` | SERIAL | PRIMARY KEY |
| `student_id` | INTEGER | FK → students, CASCADE |
| `course_id` | INTEGER | FK → courses, CASCADE |
| `internal_marks` | NUMERIC(5,2) | CHECK [0, 50] |
| `external_marks` | NUMERIC(5,2) | CHECK [0, 50] |
| `total_marks` | NUMERIC(5,2) | AUTO via trigger |
| `grade` | VARCHAR(2) | AUTO via trigger |
| — | — | UNIQUE(student_id, course_id) |

### Entity Relationships

```
students ──< enrollments >── courses
students ──< attendance  >── courses
students ──< grades      >── courses
```

- **students ↔ courses** is a **Many-to-Many** relationship, resolved through the `enrollments` junction table.
- `attendance` and `grades` are also **many-to-many bridge tables** between students and courses, with additional data columns.

---

## Normalization Analysis

### First Normal Form (1NF)
✅ All tables have a defined primary key.
✅ All columns contain atomic (indivisible) values — no multi-valued attributes.
✅ No repeating groups — attendance rows are individual records per date.

### Second Normal Form (2NF)
✅ All non-key attributes are **fully functionally dependent** on the entire primary key.
✅ `attendance` and `grades` use surrogate keys (`attendance_id`, `grade_id`) so there is no partial dependency risk.

### Third Normal Form (3NF)
✅ No transitive dependencies exist.
- `students` stores only student-specific data; department is a direct attribute, not a reference to a separate departments table (acceptable for project scope).
- `courses` stores only course-specific data.
- No non-key column depends on another non-key column.

> **Note:** A production-grade 4NF schema would extract `department` into its own lookup table. This is acknowledged and deliberately simplified for project clarity.

---

## Trigger — Auto Grade Calculation

```sql
CREATE OR REPLACE FUNCTION calculate_grade()
RETURNS TRIGGER AS $$
BEGIN
    -- Step 1: Sum the marks
    NEW.total_marks := COALESCE(NEW.internal_marks, 0)
                     + COALESCE(NEW.external_marks, 0);

    -- Step 2: Assign letter grade (out of 100)
    NEW.grade := CASE
        WHEN NEW.total_marks >= 90 THEN 'O'   -- Outstanding
        WHEN NEW.total_marks >= 80 THEN 'A'   -- Excellent
        WHEN NEW.total_marks >= 70 THEN 'B'   -- Good
        WHEN NEW.total_marks >= 60 THEN 'C'   -- Average
        WHEN NEW.total_marks >= 50 THEN 'D'   -- Pass
        ELSE 'F'                              -- Fail
    END;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_calculate_grade
BEFORE INSERT OR UPDATE ON grades
FOR EACH ROW EXECUTE FUNCTION calculate_grade();
```

**How it works:**
- Fires **BEFORE** every `INSERT` or `UPDATE` on the `grades` table.
- Modifies the `NEW` row tuple in-place before it is written to disk.
- The Flask application only supplies `internal_marks` and `external_marks` — the trigger handles the rest automatically.
- This is a classic example of **database-level business logic** enforcement.

### Grade Scale

| Grade | Range | Meaning |
|-------|-------|---------|
| O | ≥ 90 | Outstanding |
| A | ≥ 80 | Excellent |
| B | ≥ 70 | Good |
| C | ≥ 60 | Average |
| D | ≥ 50 | Pass |
| F | < 50 | Fail |

---

## Views

### `v_attendance_summary`

A complex aggregation view joining `students`, `enrollments`, `courses`, and `attendance`:

```sql
CREATE VIEW v_attendance_summary AS
SELECT
    s.student_id, s.name AS student_name, s.department,
    c.course_id, c.course_name, c.course_code,
    COUNT(a.attendance_id)                                            AS total_classes,
    SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END)            AS present_count,
    SUM(CASE WHEN a.status = 'Absent'  THEN 1 ELSE 0 END)            AS absent_count,
    SUM(CASE WHEN a.status = 'Late'    THEN 1 ELSE 0 END)            AS late_count,
    ROUND(
        (SUM(CASE WHEN a.status IN ('Present','Late') THEN 1 ELSE 0 END) * 100.0)
        / NULLIF(COUNT(a.attendance_id), 0), 2
    ) AS attendance_percentage
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
JOIN courses    c ON c.course_id  = e.course_id
LEFT JOIN attendance a
       ON a.student_id = s.student_id AND a.course_id = c.course_id
GROUP BY s.student_id, s.name, s.department,
         c.course_id, c.course_name, c.course_code;
```

**Key design decisions:**
- Uses `LEFT JOIN` on `attendance` so enrolled students with zero attendance still appear (with `NULL` percentage).
- `NULLIF(..., 0)` prevents division-by-zero when no classes have been held.
- `Late` is counted as attended (industry-standard policy).

### `v_grade_summary`

A simpler join view providing a flat, denormalized view of grades with student and course context — used by the Reports section.

---

## Indexes & Performance

| Index Name | Table | Column(s) | Purpose |
|------------|-------|-----------|---------|
| `idx_attendance_student` | attendance | student_id | Fast student attendance lookup |
| `idx_attendance_course` | attendance | course_id | Fast course attendance lookup |
| `idx_attendance_date` | attendance | date | Fast date-range filtering |
| `idx_grades_student` | grades | student_id | Fast student grade lookup |
| `idx_grades_course` | grades | course_id | Fast course grade lookup |
| `idx_enrollments_student` | enrollments | student_id | Fast enrollment lookup |
| `idx_enrollments_course` | enrollments | course_id | Fast enrollment lookup |

All are **B-tree indexes** (PostgreSQL default), optimal for equality and range queries.

> **Why these columns?** They are the most frequent `WHERE` clause predicates in the application's filter queries and the `JOIN` conditions in both views.

---

## Backend — Flask Application

### Connection Model (`db_config.py`)

```python
def query_db(sql, params=None, fetchone=False):
    """Execute SELECT → return list of RealDictRows (or one row)."""
    conn = get_connection()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchone() if fetchone else cur.fetchall()

def execute_db(sql, params=None):
    """Execute INSERT/UPDATE/DELETE with auto-commit and rollback on error."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
```

**Design highlights:**
- `RealDictCursor` returns rows as dictionaries → Jinja2 can access `{{ row.column_name }}` directly.
- Each request opens a fresh connection and closes it after use — simple and reliable for a single-process dev server.
- Parameterized queries (`%s`) prevent **SQL injection** attacks.

### Route Summary

| Route | Methods | Function |
|-------|---------|----------|
| `/` | GET | Dashboard with 5 stat cards, charts, tables |
| `/students` | GET | List all students |
| `/students/add` | GET, POST | Add student form |
| `/students/edit/<id>` | GET, POST | Edit student |
| `/students/delete/<id>` | POST | Delete student (cascade) |
| `/courses` | GET | List all courses |
| `/courses/add` | GET, POST | Add course |
| `/courses/edit/<id>` | GET, POST | Edit course |
| `/courses/delete/<id>` | POST | Delete course |
| `/enrollments` | GET | List + form on same page |
| `/enrollments/add` | POST | Enroll student |
| `/enrollments/delete/<id>` | POST | Remove enrollment |
| `/attendance` | GET | Filter & view records |
| `/attendance/mark` | GET, POST | AJAX-powered bulk marking |
| `/attendance/delete/<id>` | POST | Delete one record |
| `/grades` | GET | Filter & view grades |
| `/grades/entry` | GET, POST | UPSERT grade record |
| `/grades/delete/<id>` | POST | Delete grade |
| `/reports` | GET | Reports index |
| `/reports/attendance` | GET | Attendance summary |
| `/reports/grades` | GET | Grade summary |
| `/reports/top_students` | GET | Student rankings |
| `/reports/low_attendance` | GET | At-risk alert |
| `/api/enrolled_students` | GET | JSON API for AJAX |

---

## Frontend — UI Design

### Design System

- **Color Palette:** Deep navy dark mode (`#0f0f1a` background), indigo primary (`#4f46e5`), cyan accent (`#06b6d4`).
- **Typography:** Inter (body) + Outfit (headings/numbers) from Google Fonts.
- **Layout:** Fixed sidebar (260px) + scrollable main content area.
- **Theme:** Glassmorphism-inspired cards with `backdrop-filter`, gradient icons, subtle borders.

### Interactive Features

| Feature | Implementation |
|---------|---------------|
| Animated stat counters | JS `setInterval` counting from 0 → target |
| Attendance progress bars | CSS width animated from 0% → actual % |
| AJAX student loading | `fetch('/api/enrolled_students')` → DOM update |
| Live grade preview | JS `input` event → real-time total + grade badge |
| Auto-dismiss alerts | `setTimeout` → fade out after 4 seconds |
| Mobile sidebar | CSS transform toggle + overlay backdrop |
| Delete confirmation | `confirm()` dialog via `.btn-delete-confirm` class |

---

## Features Walkthrough

### Dashboard
- **5 stat cards:** Total Students, Courses, Enrollments, Attendance Records, Low Attendance Count
- **Attendance bar chart:** Per-course average percentage with color-coded progress bars (green ≥75%, amber ≥60%, red <60%)
- **Top 5 students:** Ranked by average total marks with 🥇🥈🥉 medals
- **Grade distribution:** Visual count per letter grade
- **Low-attendance list:** Students below 75% in any course

### Mark Attendance
- Faculty selects a course → JavaScript calls `/api/enrolled_students` → renders all enrolled students instantly without a page reload
- Each student has a 3-way radio toggle: **Present / Absent / Late**
- "All Present" and "All Absent" bulk-set buttons
- Submits via `ON CONFLICT DO UPDATE` — re-marking is safe

### Grade Entry
- Faculty enters internal (0–50) and external (0–50) marks
- **Live preview:** As marks are typed, JavaScript computes total and shows the letter grade badge in real-time
- PostgreSQL trigger auto-fills `total_marks` and `grade` on save

### Reports
| Report | Key SQL Concept |
|--------|----------------|
| Attendance Report | `v_attendance_summary` view, threshold filter |
| Grade Summary | `v_grade_summary` view + `GROUP BY` course stats |
| Top Students | `AVG`, `MAX`, `MIN` with `ORDER BY avg_marks DESC` |
| Low Attendance | View filter with `attendance_percentage < threshold` |

---

## API Endpoint

### `GET /api/enrolled_students`

Returns enrolled students for a given course and date, including their current attendance status.

**Query Parameters:**

| Param | Required | Description |
|-------|----------|-------------|
| `course_id` | Yes | The course to fetch students for |
| `date` | No | Date to check existing attendance (defaults to today) |

**Response (JSON array):**
```json
[
  {
    "student_id": 1,
    "name": "Aarav Sharma",
    "status": "Present"
  },
  {
    "student_id": 2,
    "name": "Priya Mehta",
    "status": "Absent"
  }
]
```

`status` reflects any previously marked attendance for that date (defaults to `"Present"` if not yet marked).

---

## Project File Structure

```
Yoshita/
│
├── app.py                    ← 552 lines — all Flask routes
├── db_config.py              ← DB connection + query/execute helpers
├── schema.sql                ← Full DDL: 5 tables, 1 trigger, 2 views, 7 indexes
├── sample_data.sql           ← 10 students, 5 courses, 23 enrollments,
│                               124 attendance records, 23 grades
├── setup_db.py               ← One-shot DB setup script
├── audit.py                  ← 60-check automated project verifier
├── requirements.txt          ← Python package versions
├── .env                      ← DB credentials (not committed to VCS)
├── SETUP_AND_RUN.md          ← This setup guide
├── README.md                 ← Full project documentation
│
├── static/
│   ├── style.css             ← 649 lines — full custom dark-mode CSS
│   └── main.js               ← 116 lines — sidebar, AJAX, counters, animations
│
└── templates/                ← 16 Jinja2 HTML templates
    ├── base.html             ← Layout shell (sidebar, topbar, flash messages)
    ├── dashboard.html        ← Home page with charts and analytics
    ├── students.html         ← Student list with avatar initials
    ├── student_form.html     ← Add / Edit student form
    ├── courses.html          ← Course list with code badges
    ├── course_form.html      ← Add / Edit course form
    ├── enrollments.html      ← Side-by-side form + table layout
    ├── attendance.html       ← Filtered attendance records
    ├── mark_attendance.html  ← AJAX-powered attendance marking
    ├── grades.html           ← Filtered grade records
    ├── grade_entry.html      ← Grade form with live preview
    ├── reports.html          ← Report selection cards
    ├── report_attendance.html← Attendance summary table
    ├── report_grades.html    ← Per-course stat cards + individual table
    ├── report_top_students.html← Podium display + full rankings
    └── report_low_attendance.html← At-risk list with shortfall %
```

---

## Sample Data

The included `sample_data.sql` provides a realistic demo dataset:

| Entity | Count | Details |
|--------|-------|---------|
| Students | 10 | Across CS, Electronics, Mechanical departments |
| Courses | 5 | CS301, CS201, EC201, ME201, CS401 (3–4 credits each) |
| Enrollments | 23 | Students enrolled in 2–3 courses each |
| Attendance records | 124 | Jan 2026, mixed Present/Absent/Late statuses |
| Grade records | 23 | Trigger auto-calculated totals and letter grades |

Attendance is deliberately varied so the Low Attendance report (< 75%) has meaningful data to display.

---

## Audit Results

Running `python audit.py` against the fully set-up project produces:

```
=======================================================
  SAGMS — Full Project Audit
=======================================================

[1] Tables
  [PASS]  students: 11 rows
  [PASS]  courses: 5 rows
  [PASS]  enrollments: 23 rows
  [PASS]  attendance: 124 rows
  [PASS]  grades: 23 rows

[2] Views
  [PASS]  v_attendance_summary  (23 rows)
  [PASS]  v_grade_summary  (23 rows)

[3] Trigger
  [PASS]  trg_calculate_grade

[4] Trigger correctness
  [PASS]  Auto-grade: total=87.0 -> grade=A

[5] Indexes
  [PASS]  idx_attendance_course
  [PASS]  idx_attendance_date
  [PASS]  idx_attendance_student
  [PASS]  idx_enrollments_course
  [PASS]  idx_enrollments_student
  [PASS]  idx_grades_course
  [PASS]  idx_grades_student

[6] Unique constraints
  [PASS]  No duplicate attendance records
  [PASS]  No duplicate grade records

[7] Referential integrity (FK)
  [PASS]  No orphan attendance rows
  [PASS]  No orphan grade rows

[8] Template files
  [PASS]  base.html ... report_low_attendance.html (all 16)

[9] Flask routes
  [PASS]  All 25 endpoints registered

=======================================================
  RESULT: 60/60 checks passed
  STATUS: ALL CLEAR - Project is complete!
=======================================================
```

---

## Academic Context

This project was built to fulfil the requirements of a Final-Year DBMS course, demonstrating:

- **Relational Algebra** concepts (joins, projections, selections) implemented as SQL
- **Transaction management** (auto-commit, explicit rollback on error)
- **Data integrity** at the database level via constraints and triggers
- **Aggregation and reporting** via views and GROUP BY queries
- **Web integration** of a relational database through a Python backend
- **Normalized schema design** up to Third Normal Form (3NF)

---

*Built with Flask + PostgreSQL + Vanilla CSS | Academic Project 2025–26*
