-- ============================================================
-- Student Attendance and Grade Management System
-- PostgreSQL Schema (3NF Normalized)
-- ============================================================

-- Drop tables if they exist (in correct order for FK constraints)
DROP VIEW IF EXISTS v_grade_summary CASCADE;
DROP VIEW IF EXISTS v_attendance_summary CASCADE;
DROP TABLE IF EXISTS grades CASCADE;
DROP TABLE IF EXISTS attendance CASCADE;
DROP TABLE IF EXISTS enrollments CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS students CASCADE;

-- ============================================================
-- TABLE: students
-- ============================================================
CREATE TABLE students (
    student_id   SERIAL PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    email        VARCHAR(150) NOT NULL UNIQUE,
    department   VARCHAR(100) NOT NULL,
    phone        VARCHAR(15),
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLE: courses
-- ============================================================
CREATE TABLE courses (
    course_id    SERIAL PRIMARY KEY,
    course_name  VARCHAR(150) NOT NULL,
    course_code  VARCHAR(20)  NOT NULL UNIQUE,
    credits      INTEGER      NOT NULL CHECK (credits > 0),
    department   VARCHAR(100),
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLE: enrollments  (many-to-many: students <-> courses)
-- ============================================================
CREATE TABLE enrollments (
    enrollment_id  SERIAL PRIMARY KEY,
    student_id     INTEGER NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    course_id      INTEGER NOT NULL REFERENCES courses(course_id)  ON DELETE CASCADE,
    enrolled_on    DATE DEFAULT CURRENT_DATE,
    UNIQUE (student_id, course_id)
);

-- ============================================================
-- TABLE: attendance
-- ============================================================
CREATE TABLE attendance (
    attendance_id  SERIAL PRIMARY KEY,
    student_id     INTEGER NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    course_id      INTEGER NOT NULL REFERENCES courses(course_id)  ON DELETE CASCADE,
    date           DATE    NOT NULL,
    status         VARCHAR(10) NOT NULL CHECK (status IN ('Present', 'Absent', 'Late')),
    UNIQUE (student_id, course_id, date)
);

-- ============================================================
-- TABLE: grades
-- ============================================================
CREATE TABLE grades (
    grade_id        SERIAL PRIMARY KEY,
    student_id      INTEGER NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    course_id       INTEGER NOT NULL REFERENCES courses(course_id)  ON DELETE CASCADE,
    internal_marks  NUMERIC(5,2) CHECK (internal_marks >= 0 AND internal_marks <= 50),
    external_marks  NUMERIC(5,2) CHECK (external_marks >= 0 AND external_marks <= 50),
    total_marks     NUMERIC(5,2),
    grade           VARCHAR(2),
    UNIQUE (student_id, course_id)
);

-- ============================================================
-- INDEXES for performance
-- ============================================================
CREATE INDEX idx_attendance_student   ON attendance(student_id);
CREATE INDEX idx_attendance_course    ON attendance(course_id);
CREATE INDEX idx_attendance_date      ON attendance(date);
CREATE INDEX idx_grades_student       ON grades(student_id);
CREATE INDEX idx_grades_course        ON grades(course_id);
CREATE INDEX idx_enrollments_student  ON enrollments(student_id);
CREATE INDEX idx_enrollments_course   ON enrollments(course_id);

-- ============================================================
-- TRIGGER FUNCTION: auto-calculate total_marks and grade
-- ============================================================
CREATE OR REPLACE FUNCTION calculate_grade()
RETURNS TRIGGER AS $$
BEGIN
    -- Calculate total marks
    NEW.total_marks := COALESCE(NEW.internal_marks, 0) + COALESCE(NEW.external_marks, 0);

    -- Assign letter grade based on total marks (out of 100)
    NEW.grade := CASE
        WHEN NEW.total_marks >= 90 THEN 'O'
        WHEN NEW.total_marks >= 80 THEN 'A'
        WHEN NEW.total_marks >= 70 THEN 'B'
        WHEN NEW.total_marks >= 60 THEN 'C'
        WHEN NEW.total_marks >= 50 THEN 'D'
        ELSE 'F'
    END;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach trigger to grades table
CREATE TRIGGER trg_calculate_grade
BEFORE INSERT OR UPDATE ON grades
FOR EACH ROW
EXECUTE FUNCTION calculate_grade();

-- ============================================================
-- VIEW: v_attendance_summary
-- ============================================================
CREATE VIEW v_attendance_summary AS
SELECT
    s.student_id,
    s.name              AS student_name,
    s.department,
    c.course_id,
    c.course_name,
    c.course_code,
    COUNT(a.attendance_id)                                         AS total_classes,
    SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END)         AS present_count,
    SUM(CASE WHEN a.status = 'Absent'  THEN 1 ELSE 0 END)         AS absent_count,
    SUM(CASE WHEN a.status = 'Late'    THEN 1 ELSE 0 END)         AS late_count,
    ROUND(
        (SUM(CASE WHEN a.status IN ('Present','Late') THEN 1 ELSE 0 END) * 100.0)
        / NULLIF(COUNT(a.attendance_id), 0), 2
    )                                                               AS attendance_percentage
FROM students  s
JOIN enrollments e ON s.student_id = e.student_id
JOIN courses   c   ON c.course_id  = e.course_id
LEFT JOIN attendance a ON a.student_id = s.student_id
                      AND a.course_id  = c.course_id
GROUP BY s.student_id, s.name, s.department, c.course_id, c.course_name, c.course_code;

-- ============================================================
-- VIEW: v_grade_summary
-- ============================================================
CREATE VIEW v_grade_summary AS
SELECT
    s.student_id,
    s.name              AS student_name,
    s.department,
    c.course_id,
    c.course_name,
    c.course_code,
    c.credits,
    g.internal_marks,
    g.external_marks,
    g.total_marks,
    g.grade
FROM students  s
JOIN grades    g ON g.student_id = s.student_id
JOIN courses   c ON c.course_id  = g.course_id;
