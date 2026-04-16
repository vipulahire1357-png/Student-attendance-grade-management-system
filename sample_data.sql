-- ============================================================
-- Sample Data for Student Attendance & Grade Management System
-- ============================================================

-- Students
INSERT INTO students (name, email, department, phone) VALUES
('Aarav Sharma',    'aarav.sharma@college.edu',    'Computer Science', '9876543210'),
('Priya Mehta',     'priya.mehta@college.edu',     'Computer Science', '9876543211'),
('Rohit Verma',     'rohit.verma@college.edu',     'Electronics',      '9876543212'),
('Sneha Patil',     'sneha.patil@college.edu',     'Electronics',      '9876543213'),
('Arjun Nair',      'arjun.nair@college.edu',      'Computer Science', '9876543214'),
('Kavya Reddy',     'kavya.reddy@college.edu',     'Mechanical',       '9876543215'),
('Vikram Singh',    'vikram.singh@college.edu',    'Computer Science', '9876543216'),
('Ananya Das',      'ananya.das@college.edu',      'Electronics',      '9876543217'),
('Riya Joshi',      'riya.joshi@college.edu',      'Mechanical',       '9876543218'),
('Karan Patel',     'karan.patel@college.edu',     'Computer Science', '9876543219');

-- Courses
INSERT INTO courses (course_name, course_code, credits, department) VALUES
('Database Management Systems',     'CS301', 4, 'Computer Science'),
('Data Structures and Algorithms',  'CS201', 4, 'Computer Science'),
('Digital Electronics',             'EC201', 3, 'Electronics'),
('Thermodynamics',                  'ME201', 3, 'Mechanical'),
('Computer Networks',               'CS401', 3, 'Computer Science');

-- Enrollments
INSERT INTO enrollments (student_id, course_id) VALUES
(1, 1),(1, 2),(1, 5),
(2, 1),(2, 2),(2, 5),
(3, 3),(3, 1),
(4, 3),(4, 4),
(5, 1),(5, 2),(5, 5),
(6, 4),(6, 3),
(7, 1),(7, 2),
(8, 3),(8, 5),
(9, 4),
(10,1),(10,2),(10,5);

-- Attendance (mix of Present / Absent / Late)
-- Course 1 (DBMS) - CS301
INSERT INTO attendance (student_id, course_id, date, status) VALUES
(1,1,'2026-01-05','Present'),(1,1,'2026-01-07','Present'),(1,1,'2026-01-09','Absent'),
(1,1,'2026-01-12','Present'),(1,1,'2026-01-14','Present'),(1,1,'2026-01-16','Present'),
(1,1,'2026-01-19','Late'),  (1,1,'2026-01-21','Present'),(1,1,'2026-01-23','Present'),
(1,1,'2026-01-26','Absent'),

(2,1,'2026-01-05','Present'),(2,1,'2026-01-07','Absent'),(2,1,'2026-01-09','Absent'),
(2,1,'2026-01-12','Present'),(2,1,'2026-01-14','Absent'),(2,1,'2026-01-16','Present'),
(2,1,'2026-01-19','Absent'),(2,1,'2026-01-21','Present'),(2,1,'2026-01-23','Absent'),
(2,1,'2026-01-26','Present'),

(3,1,'2026-01-05','Absent'),(3,1,'2026-01-07','Absent'),(3,1,'2026-01-09','Absent'),
(3,1,'2026-01-12','Absent'),(3,1,'2026-01-14','Present'),(3,1,'2026-01-16','Absent'),
(3,1,'2026-01-19','Absent'),(3,1,'2026-01-21','Absent'),(3,1,'2026-01-23','Present'),
(3,1,'2026-01-26','Absent'),

(5,1,'2026-01-05','Present'),(5,1,'2026-01-07','Present'),(5,1,'2026-01-09','Present'),
(5,1,'2026-01-12','Present'),(5,1,'2026-01-14','Present'),(5,1,'2026-01-16','Late'),
(5,1,'2026-01-19','Present'),(5,1,'2026-01-21','Present'),(5,1,'2026-01-23','Present'),
(5,1,'2026-01-26','Present'),

(7,1,'2026-01-05','Present'),(7,1,'2026-01-07','Present'),(7,1,'2026-01-09','Present'),
(7,1,'2026-01-12','Absent'),(7,1,'2026-01-14','Present'),(7,1,'2026-01-16','Present'),
(7,1,'2026-01-19','Present'),(7,1,'2026-01-21','Absent'),(7,1,'2026-01-23','Present'),
(7,1,'2026-01-26','Present'),

(10,1,'2026-01-05','Present'),(10,1,'2026-01-07','Present'),(10,1,'2026-01-09','Present'),
(10,1,'2026-01-12','Present'),(10,1,'2026-01-14','Present'),(10,1,'2026-01-16','Present'),
(10,1,'2026-01-19','Present'),(10,1,'2026-01-21','Present'),(10,1,'2026-01-23','Late'),
(10,1,'2026-01-26','Present');

-- Course 2 (DSA) - CS201
INSERT INTO attendance (student_id, course_id, date, status) VALUES
(1,2,'2026-01-06','Present'),(1,2,'2026-01-08','Present'),(1,2,'2026-01-10','Present'),
(1,2,'2026-01-13','Present'),(1,2,'2026-01-15','Absent'),(1,2,'2026-01-17','Present'),
(1,2,'2026-01-20','Present'),(1,2,'2026-01-22','Present'),

(2,2,'2026-01-06','Absent'),(2,2,'2026-01-08','Absent'),(2,2,'2026-01-10','Present'),
(2,2,'2026-01-13','Absent'),(2,2,'2026-01-15','Absent'),(2,2,'2026-01-17','Present'),
(2,2,'2026-01-20','Absent'),(2,2,'2026-01-22','Absent'),

(5,2,'2026-01-06','Present'),(5,2,'2026-01-08','Present'),(5,2,'2026-01-10','Present'),
(5,2,'2026-01-13','Present'),(5,2,'2026-01-15','Present'),(5,2,'2026-01-17','Present'),
(5,2,'2026-01-20','Present'),(5,2,'2026-01-22','Present'),

(7,2,'2026-01-06','Present'),(7,2,'2026-01-08','Late'),(7,2,'2026-01-10','Present'),
(7,2,'2026-01-13','Present'),(7,2,'2026-01-15','Present'),(7,2,'2026-01-17','Absent'),
(7,2,'2026-01-20','Present'),(7,2,'2026-01-22','Present'),

(10,2,'2026-01-06','Present'),(10,2,'2026-01-08','Present'),(10,2,'2026-01-10','Present'),
(10,2,'2026-01-13','Present'),(10,2,'2026-01-15','Present'),(10,2,'2026-01-17','Present'),
(10,2,'2026-01-20','Present'),(10,2,'2026-01-22','Present');

-- Course 3 (Digital Electronics)
INSERT INTO attendance (student_id, course_id, date, status) VALUES
(3,3,'2026-01-06','Present'),(3,3,'2026-01-08','Absent'),(3,3,'2026-01-13','Present'),
(3,3,'2026-01-15','Present'),(3,3,'2026-01-20','Absent'),(3,3,'2026-01-22','Present'),

(4,3,'2026-01-06','Present'),(4,3,'2026-01-08','Present'),(4,3,'2026-01-13','Present'),
(4,3,'2026-01-15','Late'),(4,3,'2026-01-20','Present'),(4,3,'2026-01-22','Present'),

(6,3,'2026-01-06','Absent'),(6,3,'2026-01-08','Absent'),(6,3,'2026-01-13','Absent'),
(6,3,'2026-01-15','Absent'),(6,3,'2026-01-20','Present'),(6,3,'2026-01-22','Present'),

(8,3,'2026-01-06','Present'),(8,3,'2026-01-08','Present'),(8,3,'2026-01-13','Present'),
(8,3,'2026-01-15','Present'),(8,3,'2026-01-20','Present'),(8,3,'2026-01-22','Present');

-- Grades (trigger will auto-calculate total_marks and grade)
INSERT INTO grades (student_id, course_id, internal_marks, external_marks) VALUES
(1,  1, 44, 43),
(2,  1, 30, 30),
(3,  1, 15, 20),
(5,  1, 46, 47),
(7,  1, 38, 40),
(10, 1, 48, 49),

(1,  2, 42, 41),
(2,  2, 25, 28),
(5,  2, 49, 48),
(7,  2, 36, 37),
(10, 2, 47, 45),

(3,  3, 38, 35),
(4,  3, 40, 42),
(6,  3, 22, 25),
(8,  3, 45, 44),

(4,  4, 38, 36),
(6,  4, 30, 32),
(9,  4, 42, 40),

(1,  5, 41, 43),
(2,  5, 28, 30),
(5,  5, 44, 46),
(8,  5, 38, 36),
(10, 5, 46, 48);
