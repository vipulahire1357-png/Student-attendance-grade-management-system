"""audit.py — Full project health check."""
from dotenv import load_dotenv
load_dotenv()
from db_config import query_db

PASS = "[PASS]"
FAIL = "[FAIL]"
results = []

def check(label, ok, detail=""):
    status = PASS if ok else FAIL
    line = f"  {status}  {label}" + (f"  ({detail})" if detail else "")
    results.append((ok, line))
    print(line)

print("=" * 55)
print("  SAGMS — Full Project Audit")
print("=" * 55)

# ── 1. TABLE ROW COUNTS ──────────────────────────────────────
print("\n[1] Tables")
expected = {"students": 10, "courses": 5, "enrollments": 23,
            "attendance": 124, "grades": 23}
for tbl, exp in expected.items():
    try:
        n = query_db(f"SELECT COUNT(*) AS c FROM {tbl}", fetchone=True)["c"]
        check(f"{tbl}: {n} rows", n > 0, f"expected ~{exp}")
    except Exception as e:
        check(tbl, False, str(e))

# ── 2. VIEWS ─────────────────────────────────────────────────
print("\n[2] Views")
for v in ["v_attendance_summary", "v_grade_summary"]:
    try:
        n = query_db(f"SELECT COUNT(*) AS c FROM {v}", fetchone=True)["c"]
        check(v, True, f"{n} rows")
    except Exception as e:
        check(v, False, str(e))

# ── 3. TRIGGER ───────────────────────────────────────────────
print("\n[3] Trigger")
try:
    r = query_db(
        "SELECT trigger_name FROM information_schema.triggers "
        "WHERE trigger_name = %s",
        ("trg_calculate_grade",), fetchone=True
    )
    check("trg_calculate_grade", bool(r))
except Exception as e:
    check("trg_calculate_grade", False, str(e))

# ── 4. TRIGGER CORRECTNESS (grade auto-set) ───────────────────
print("\n[4] Trigger correctness")
try:
    row = query_db(
        "SELECT total_marks, grade FROM grades "
        "WHERE total_marks IS NOT NULL LIMIT 1",
        fetchone=True
    )
    if row:
        tm = float(row["total_marks"])
        expected_grade = (
            "O" if tm >= 90 else "A" if tm >= 80 else "B" if tm >= 70
            else "C" if tm >= 60 else "D" if tm >= 50 else "F"
        )
        check(
            f"Auto-grade: total={tm} -> grade={row['grade']}",
            row["grade"] == expected_grade
        )
    else:
        check("Auto-grade (no data)", False)
except Exception as e:
    check("Auto-grade", False, str(e))

# ── 5. INDEXES ───────────────────────────────────────────────
print("\n[5] Indexes")
try:
    rows = query_db(
        "SELECT indexname FROM pg_indexes "
        "WHERE tablename IN ('students','courses','enrollments','attendance','grades') "
        "AND indexname LIKE 'idx_%' ORDER BY indexname"
    )
    for r in rows:
        check(r["indexname"], True)
    if not rows:
        check("Indexes", False, "none found")
except Exception as e:
    check("Indexes", False, str(e))

# ── 6. UNIQUE CONSTRAINTS ────────────────────────────────────
print("\n[6] Unique constraints (duplicate prevention)")
try:
    # check unique on attendance
    r = query_db(
        "SELECT COUNT(*) AS c FROM ("
        "  SELECT student_id, course_id, date, COUNT(*) "
        "  FROM attendance GROUP BY student_id, course_id, date "
        "  HAVING COUNT(*) > 1"
        ") x",
        fetchone=True
    )
    check("No duplicate attendance records", r["c"] == 0, f"{r['c']} dupes")

    r = query_db(
        "SELECT COUNT(*) AS c FROM ("
        "  SELECT student_id, course_id, COUNT(*) "
        "  FROM grades GROUP BY student_id, course_id "
        "  HAVING COUNT(*) > 1"
        ") x",
        fetchone=True
    )
    check("No duplicate grade records", r["c"] == 0, f"{r['c']} dupes")
except Exception as e:
    check("Unique constraints", False, str(e))

# ── 7. FK CASCADE CHECK ──────────────────────────────────────
print("\n[7] Referential integrity (FK)")
try:
    # Orphan attendance records
    r = query_db(
        "SELECT COUNT(*) AS c FROM attendance a "
        "LEFT JOIN students s ON s.student_id = a.student_id "
        "WHERE s.student_id IS NULL",
        fetchone=True
    )
    check("No orphan attendance rows", r["c"] == 0)
    r = query_db(
        "SELECT COUNT(*) AS c FROM grades g "
        "LEFT JOIN students s ON s.student_id = g.student_id "
        "WHERE s.student_id IS NULL",
        fetchone=True
    )
    check("No orphan grade rows", r["c"] == 0)
except Exception as e:
    check("FK integrity", False, str(e))

# ── 8. TEMPLATES FILES ───────────────────────────────────────
print("\n[8] Template files")
import os
tmpl_dir = os.path.join(os.path.dirname(__file__), "templates")
required_templates = [
    "base.html", "dashboard.html", "students.html", "student_form.html",
    "courses.html", "course_form.html", "enrollments.html",
    "attendance.html", "mark_attendance.html",
    "grades.html", "grade_entry.html",
    "reports.html", "report_attendance.html", "report_grades.html",
    "report_top_students.html", "report_low_attendance.html"
]
for t in required_templates:
    path = os.path.join(tmpl_dir, t)
    check(t, os.path.exists(path) and os.path.getsize(path) > 200)

# ── 9. FLASK ROUTES ──────────────────────────────────────────
print("\n[9] Flask routes registered")
import app as flask_app
rules = {rule.endpoint: str(rule) for rule in flask_app.app.url_map.iter_rules()}
expected_endpoints = [
    "dashboard", "students", "add_student", "edit_student", "delete_student",
    "courses", "add_course", "edit_course", "delete_course",
    "enrollments", "add_enrollment", "delete_enrollment",
    "attendance", "mark_attendance", "delete_attendance", "api_enrolled_students",
    "grades", "grade_entry", "delete_grade",
    "reports", "report_attendance", "report_grades",
    "report_top_students", "report_low_attendance"
]
for ep in expected_endpoints:
    check(f"/{ep}", ep in rules, rules.get(ep, "MISSING"))

# ── SUMMARY ──────────────────────────────────────────────────
total  = len(results)
passed = sum(1 for ok, _ in results if ok)
failed = total - passed

print()
print("=" * 55)
print(f"  RESULT: {passed}/{total} checks passed")
if failed == 0:
    print("  STATUS: ALL CLEAR - Project is complete!")
else:
    print(f"  STATUS: {failed} issue(s) need attention")
print("=" * 55)
