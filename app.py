"""
Student Attendance and Grade Management System
Flask Application Entry Point
"""

import os
from datetime import date, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from dotenv import load_dotenv
from db_config import query_db, execute_db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-2026")


@app.context_processor
def inject_now():
    return {"now": date.today().strftime("%d %b %Y")}


# ─────────────────────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────────────────────
@app.route("/")
def dashboard():
    stats = {
        "total_students":  query_db("SELECT COUNT(*) AS c FROM students",     fetchone=True)["c"],
        "total_courses":   query_db("SELECT COUNT(*) AS c FROM courses",      fetchone=True)["c"],
        "total_enrollments": query_db("SELECT COUNT(*) AS c FROM enrollments", fetchone=True)["c"],
        "total_attendance":  query_db("SELECT COUNT(*) AS c FROM attendance",  fetchone=True)["c"],
    }

    # Avg attendance % per course (from view)
    course_attendance = query_db("""
        SELECT course_name, course_code,
               ROUND(AVG(attendance_percentage), 2) AS avg_pct
        FROM   v_attendance_summary
        GROUP  BY course_name, course_code
        ORDER  BY avg_pct DESC
    """)

    # Top 5 students by avg total marks
    top_students = query_db("""
        SELECT s.name, s.department,
               ROUND(AVG(g.total_marks), 2) AS avg_marks
        FROM   grades   g
        JOIN   students s ON s.student_id = g.student_id
        GROUP  BY s.student_id, s.name, s.department
        ORDER  BY avg_marks DESC
        LIMIT  5
    """)

    # Students below 75 % attendance in any course
    low_att = query_db("""
        SELECT DISTINCT student_name, department
        FROM   v_attendance_summary
        WHERE  attendance_percentage < 75
        ORDER  BY student_name
    """)

    # Grade distribution
    grade_dist = query_db("""
        SELECT grade, COUNT(*) AS cnt
        FROM   grades
        WHERE  grade IS NOT NULL
        GROUP  BY grade
        ORDER  BY grade
    """)

    return render_template("dashboard.html",
                           stats=stats,
                           course_attendance=course_attendance,
                           top_students=top_students,
                           low_att=low_att,
                           grade_dist=grade_dist)


# ─────────────────────────────────────────────────────────────
# STUDENTS
# ─────────────────────────────────────────────────────────────
@app.route("/students")
def students():
    rows = query_db("SELECT * FROM students ORDER BY student_id")
    return render_template("students.html", students=rows)


@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name  = request.form["name"].strip()
        email = request.form["email"].strip()
        dept  = request.form["department"].strip()
        phone = request.form.get("phone", "").strip()
        try:
            execute_db(
                "INSERT INTO students (name, email, department, phone) VALUES (%s,%s,%s,%s)",
                (name, email, dept, phone or None)
            )
            flash("Student added successfully!", "success")
        except Exception as e:
            flash(f"Error: {e}", "danger")
        return redirect(url_for("students"))
    return render_template("student_form.html", action="add", student=None)


@app.route("/students/edit/<int:sid>", methods=["GET", "POST"])
def edit_student(sid):
    student = query_db("SELECT * FROM students WHERE student_id=%s", (sid,), fetchone=True)
    if not student:
        flash("Student not found.", "warning")
        return redirect(url_for("students"))

    if request.method == "POST":
        name  = request.form["name"].strip()
        email = request.form["email"].strip()
        dept  = request.form["department"].strip()
        phone = request.form.get("phone", "").strip()
        try:
            execute_db(
                "UPDATE students SET name=%s, email=%s, department=%s, phone=%s WHERE student_id=%s",
                (name, email, dept, phone or None, sid)
            )
            flash("Student updated successfully!", "success")
        except Exception as e:
            flash(f"Error: {e}", "danger")
        return redirect(url_for("students"))
    return render_template("student_form.html", action="edit", student=student)


@app.route("/students/delete/<int:sid>", methods=["POST"])
def delete_student(sid):
    try:
        execute_db("DELETE FROM students WHERE student_id=%s", (sid,))
        flash("Student deleted.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("students"))


# ─────────────────────────────────────────────────────────────
# COURSES
# ─────────────────────────────────────────────────────────────
@app.route("/courses")
def courses():
    rows = query_db("SELECT * FROM courses ORDER BY course_id")
    return render_template("courses.html", courses=rows)


@app.route("/courses/add", methods=["GET", "POST"])
def add_course():
    if request.method == "POST":
        name    = request.form["course_name"].strip()
        code    = request.form["course_code"].strip()
        credits = request.form["credits"].strip()
        dept    = request.form.get("department", "").strip()
        try:
            execute_db(
                "INSERT INTO courses (course_name, course_code, credits, department) VALUES (%s,%s,%s,%s)",
                (name, code, int(credits), dept or None)
            )
            flash("Course added successfully!", "success")
        except Exception as e:
            flash(f"Error: {e}", "danger")
        return redirect(url_for("courses"))
    return render_template("course_form.html", action="add", course=None)


@app.route("/courses/edit/<int:cid>", methods=["GET", "POST"])
def edit_course(cid):
    course = query_db("SELECT * FROM courses WHERE course_id=%s", (cid,), fetchone=True)
    if not course:
        flash("Course not found.", "warning")
        return redirect(url_for("courses"))

    if request.method == "POST":
        name    = request.form["course_name"].strip()
        code    = request.form["course_code"].strip()
        credits = request.form["credits"].strip()
        dept    = request.form.get("department", "").strip()
        try:
            execute_db(
                "UPDATE courses SET course_name=%s, course_code=%s, credits=%s, department=%s WHERE course_id=%s",
                (name, code, int(credits), dept or None, cid)
            )
            flash("Course updated!", "success")
        except Exception as e:
            flash(f"Error: {e}", "danger")
        return redirect(url_for("courses"))
    return render_template("course_form.html", action="edit", course=course)


@app.route("/courses/delete/<int:cid>", methods=["POST"])
def delete_course(cid):
    try:
        execute_db("DELETE FROM courses WHERE course_id=%s", (cid,))
        flash("Course deleted.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("courses"))


# ─────────────────────────────────────────────────────────────
# ENROLLMENTS
# ─────────────────────────────────────────────────────────────
@app.route("/enrollments")
def enrollments():
    rows = query_db("""
        SELECT e.enrollment_id, s.name AS student_name, s.department,
               c.course_name, c.course_code, e.enrolled_on
        FROM   enrollments e
        JOIN   students    s ON s.student_id = e.student_id
        JOIN   courses     c ON c.course_id  = e.course_id
        ORDER  BY e.enrollment_id
    """)
    students_list = query_db("SELECT student_id, name FROM students ORDER BY name")
    courses_list  = query_db("SELECT course_id, course_name, course_code FROM courses ORDER BY course_name")
    return render_template("enrollments.html",
                           enrollments=rows,
                           students=students_list,
                           courses=courses_list)


@app.route("/enrollments/add", methods=["POST"])
def add_enrollment():
    student_id = request.form["student_id"]
    course_id  = request.form["course_id"]
    try:
        execute_db(
            "INSERT INTO enrollments (student_id, course_id) VALUES (%s,%s)",
            (student_id, course_id)
        )
        flash("Student enrolled successfully!", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("enrollments"))


@app.route("/enrollments/delete/<int:eid>", methods=["POST"])
def delete_enrollment(eid):
    try:
        execute_db("DELETE FROM enrollments WHERE enrollment_id=%s", (eid,))
        flash("Enrollment removed.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("enrollments"))


# ─────────────────────────────────────────────────────────────
# ATTENDANCE
# ─────────────────────────────────────────────────────────────
@app.route("/attendance")
def attendance():
    course_id  = request.args.get("course_id",  "")
    student_id = request.args.get("student_id", "")
    att_date   = request.args.get("date", "")

    sql = """
        SELECT a.attendance_id, s.name AS student_name, c.course_name,
               c.course_code, a.date, a.status
        FROM   attendance a
        JOIN   students   s ON s.student_id = a.student_id
        JOIN   courses    c ON c.course_id  = a.course_id
        WHERE  1=1
    """
    params = []
    if course_id:
        sql += " AND a.course_id = %s"; params.append(course_id)
    if student_id:
        sql += " AND a.student_id = %s"; params.append(student_id)
    if att_date:
        sql += " AND a.date = %s"; params.append(att_date)
    sql += " ORDER BY a.date DESC, s.name"

    records       = query_db(sql, params)
    students_list = query_db("SELECT student_id, name FROM students ORDER BY name")
    courses_list  = query_db("SELECT course_id, course_name, course_code FROM courses ORDER BY course_name")

    return render_template("attendance.html",
                           records=records,
                           students=students_list,
                           courses=courses_list,
                           sel_course=course_id,
                           sel_student=student_id,
                           sel_date=att_date)


@app.route("/attendance/mark", methods=["GET", "POST"])
def mark_attendance():
    """Mark attendance for all enrolled students in a course on a date."""
    courses_list = query_db("SELECT course_id, course_name, course_code FROM courses ORDER BY course_name")

    if request.method == "POST":
        course_id = request.form["course_id"]
        att_date  = request.form["date"]
        student_ids = request.form.getlist("student_ids")
        statuses    = request.form.getlist("statuses")

        errors = 0
        for sid, status in zip(student_ids, statuses):
            try:
                execute_db("""
                    INSERT INTO attendance (student_id, course_id, date, status)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (student_id, course_id, date)
                    DO UPDATE SET status = EXCLUDED.status
                """, (sid, course_id, att_date, status))
            except Exception:
                errors += 1

        if errors:
            flash(f"Attendance saved with {errors} error(s).", "warning")
        else:
            flash("Attendance marked successfully!", "success")
        return redirect(url_for("attendance"))

    # GET – pre-load students for selected course
    course_id = request.args.get("course_id", "")
    sel_date  = request.args.get("date", str(date.today()))
    enrolled  = []
    if course_id:
        enrolled = query_db("""
            SELECT s.student_id, s.name,
                   COALESCE(a.status, 'Present') AS status
            FROM   enrollments e
            JOIN   students    s ON s.student_id = e.student_id
            LEFT JOIN attendance a
                   ON a.student_id = e.student_id
                  AND a.course_id  = e.course_id
                  AND a.date       = %s
            WHERE  e.course_id = %s
            ORDER  BY s.name
        """, (sel_date, course_id))

    return render_template("mark_attendance.html",
                           courses=courses_list,
                           enrolled=enrolled,
                           sel_course=course_id,
                           sel_date=sel_date)


@app.route("/attendance/delete/<int:aid>", methods=["POST"])
def delete_attendance(aid):
    execute_db("DELETE FROM attendance WHERE attendance_id=%s", (aid,))
    flash("Record deleted.", "success")
    return redirect(url_for("attendance"))


# AJAX: get enrolled students for a course (used in mark_attendance)
@app.route("/api/enrolled_students")
def api_enrolled_students():
    course_id = request.args.get("course_id")
    sel_date  = request.args.get("date", str(date.today()))
    rows = query_db("""
        SELECT s.student_id, s.name,
               COALESCE(a.status, 'Present') AS status
        FROM   enrollments e
        JOIN   students    s ON s.student_id = e.student_id
        LEFT JOIN attendance a
               ON a.student_id = e.student_id
              AND a.course_id  = e.course_id
              AND a.date       = %s
        WHERE  e.course_id = %s
        ORDER  BY s.name
    """, (sel_date, course_id))
    return jsonify([dict(r) for r in rows])


# ─────────────────────────────────────────────────────────────
# GRADES
# ─────────────────────────────────────────────────────────────
@app.route("/grades")
def grades():
    course_id  = request.args.get("course_id",  "")
    student_id = request.args.get("student_id", "")

    sql = """
        SELECT g.grade_id, s.name AS student_name, s.department,
               c.course_name, c.course_code,
               g.internal_marks, g.external_marks, g.total_marks, g.grade
        FROM   grades  g
        JOIN   students s ON s.student_id = g.student_id
        JOIN   courses  c ON c.course_id  = g.course_id
        WHERE  1=1
    """
    params = []
    if course_id:
        sql += " AND g.course_id = %s"; params.append(course_id)
    if student_id:
        sql += " AND g.student_id = %s"; params.append(student_id)
    sql += " ORDER BY s.name, c.course_name"

    records       = query_db(sql, params)
    students_list = query_db("SELECT student_id, name FROM students ORDER BY name")
    courses_list  = query_db("SELECT course_id, course_name, course_code FROM courses ORDER BY course_name")

    return render_template("grades.html",
                           records=records,
                           students=students_list,
                           courses=courses_list,
                           sel_course=course_id,
                           sel_student=student_id)


@app.route("/grades/entry", methods=["GET", "POST"])
def grade_entry():
    students_list = query_db("SELECT student_id, name FROM students ORDER BY name")
    courses_list  = query_db("SELECT course_id, course_name, course_code FROM courses ORDER BY course_name")

    if request.method == "POST":
        student_id      = request.form["student_id"]
        course_id       = request.form["course_id"]
        internal_marks  = request.form["internal_marks"]
        external_marks  = request.form["external_marks"]
        try:
            execute_db("""
                INSERT INTO grades (student_id, course_id, internal_marks, external_marks)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (student_id, course_id)
                DO UPDATE SET internal_marks = EXCLUDED.internal_marks,
                              external_marks = EXCLUDED.external_marks
            """, (student_id, course_id, internal_marks, external_marks))
            flash("Grade saved (trigger auto-calculated total & letter grade)!", "success")
        except Exception as e:
            flash(f"Error: {e}", "danger")
        return redirect(url_for("grades"))

    return render_template("grade_entry.html",
                           students=students_list,
                           courses=courses_list)


@app.route("/grades/delete/<int:gid>", methods=["POST"])
def delete_grade(gid):
    execute_db("DELETE FROM grades WHERE grade_id=%s", (gid,))
    flash("Grade record deleted.", "success")
    return redirect(url_for("grades"))


# ─────────────────────────────────────────────────────────────
# REPORTS
# ─────────────────────────────────────────────────────────────
@app.route("/reports")
def reports():
    return render_template("reports.html")


@app.route("/reports/attendance")
def report_attendance():
    course_id = request.args.get("course_id", "")
    threshold = request.args.get("threshold", "75")

    sql = "SELECT * FROM v_attendance_summary WHERE 1=1"
    params = []
    if course_id:
        sql += " AND course_id = %s"; params.append(course_id)
    if threshold:
        sql += " AND (attendance_percentage < %s OR attendance_percentage IS NULL)"
        params.append(threshold)
    else:
        pass  # show all
    sql += " ORDER BY student_name, course_name"

    show_all = request.args.get("show_all", "0")
    if show_all == "1":
        sql = "SELECT * FROM v_attendance_summary WHERE 1=1"
        params = []
        if course_id:
            sql += " AND course_id = %s"; params.append(course_id)
        sql += " ORDER BY student_name, course_name"

    rows          = query_db(sql, params)
    courses_list  = query_db("SELECT course_id, course_name, course_code FROM courses ORDER BY course_name")

    return render_template("report_attendance.html",
                           rows=rows,
                           courses=courses_list,
                           sel_course=course_id,
                           threshold=threshold,
                           show_all=show_all)


@app.route("/reports/grades")
def report_grades():
    course_id = request.args.get("course_id", "")

    sql = "SELECT * FROM v_grade_summary WHERE 1=1"
    params = []
    if course_id:
        sql += " AND course_id = %s"; params.append(course_id)
    sql += " ORDER BY total_marks DESC NULLS LAST"

    rows = query_db(sql, params)

    # Avg marks per course
    avg_sql = """
        SELECT c.course_name, c.course_code,
               ROUND(AVG(g.internal_marks), 2) AS avg_internal,
               ROUND(AVG(g.external_marks), 2) AS avg_external,
               ROUND(AVG(g.total_marks),    2) AS avg_total,
               MAX(g.total_marks)               AS max_marks,
               MIN(g.total_marks)               AS min_marks
        FROM   grades  g
        JOIN   courses c ON c.course_id = g.course_id
    """
    avg_params = []
    if course_id:
        avg_sql += " WHERE g.course_id = %s"; avg_params.append(course_id)
    avg_sql += " GROUP BY c.course_name, c.course_code ORDER BY c.course_name"
    avg_rows = query_db(avg_sql, avg_params)

    courses_list = query_db("SELECT course_id, course_name, course_code FROM courses ORDER BY course_name")

    return render_template("report_grades.html",
                           rows=rows,
                           avg_rows=avg_rows,
                           courses=courses_list,
                           sel_course=course_id)


@app.route("/reports/top_students")
def report_top_students():
    rows = query_db("""
        SELECT s.student_id, s.name, s.department,
               ROUND(AVG(g.total_marks), 2)    AS avg_marks,
               COUNT(g.course_id)              AS courses_taken,
               MAX(g.total_marks)              AS highest,
               MIN(g.total_marks)              AS lowest
        FROM   grades   g
        JOIN   students s ON s.student_id = g.student_id
        GROUP  BY s.student_id, s.name, s.department
        ORDER  BY avg_marks DESC
    """)
    return render_template("report_top_students.html", rows=rows)


@app.route("/reports/low_attendance")
def report_low_attendance():
    threshold = request.args.get("threshold", "75")
    rows = query_db("""
        SELECT * FROM v_attendance_summary
        WHERE  attendance_percentage < %s
           OR  attendance_percentage IS NULL
        ORDER  BY attendance_percentage ASC NULLS FIRST
    """, (threshold,))
    return render_template("report_low_attendance.html", rows=rows, threshold=threshold)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
