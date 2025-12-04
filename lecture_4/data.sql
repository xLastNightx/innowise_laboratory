/* 
=====================================
SCHOOL DATABASE: COMPLETE SQL SCRIPT
===================================== 
*/

-- 1. CREATE TABLES
-- ---------------
-- Table: students - stores student information
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    birth_year INTEGER DEFAULT 2000
);

-- Table: grades - stores student grades with referential integrity
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject TEXT DEFAULT 'Not Selected',
    grade INTEGER CHECK (grade BETWEEN 1 AND 100),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- 2. INSERT SAMPLE DATA
-- --------------------
-- Insert 9 sample students
INSERT INTO students (full_name, birth_year) VALUES
    ('Alice Johnson', 2005),
    ('Brian Smith', 2004),
    ('Carla Reyes', 2006),
    ('Daniel Kim', 2005),
    ('Eva Thompson', 2003),
    ('Felix Nguyen', 2007),
    ('Grace Patel', 2005),
    ('Henry Lopez', 2004),
    ('Isabella Martinez', 2006);

-- Adding ratings (some can be NULL if unknown)
INSERT INTO grades (student_id, subject, grade) VALUES
    (1, 'Math', 88),
    (1, 'English', 92),
    (1, 'Science', 85),
    (2, 'Math', 75),
    (2, 'History', 83),
    (2, 'English', 79),
    (3, 'Science', 95),
    (3, 'Math', 91),
    (3, 'Art', 89),
    (4, 'Math', 84),
    (4, 'Science', 88),
    (4, 'Physical Education', 93),
    (5, 'English', 90),
    (5, 'History', 85),
    (5, 'Math', 88),
    (6, 'Science', 72),
    (6, 'Math', 78),
    (6, 'English', 81),
    (7, 'Art', 94),
    (7, 'Science', 87),
    (7, 'Math', 90),
    (8, 'History', 77),
    (8, 'Math', 83),
    (8, 'Science', 80),
    (9, 'English', 96),
    (9, 'Math', 89),
    (9, 'Art', 92);

-- 3. REQUIRED QUERIES
-- -------------------
-- Query 3: All grades for Alice Johnson
SELECT '=== Query 3: All grades for Alice Johnson ===';
SELECT s.full_name, g.subject, g.grade
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE s.full_name = 'Alice Johnson';

-- Query 4: Average grade per student
SELECT '=== Query 4: Average grade per student ===';
SELECT s.full_name, AVG(g.grade) as average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.full_name
ORDER BY average_grade DESC;

-- Query 5: Students born after 2004
SELECT '=== Query 5: Students born after 2004 ===';
SELECT id, full_name, birth_year
FROM students
WHERE birth_year > 2004
ORDER BY birth_year;

-- Query 6: Subjects and their average grades
SELECT '=== Query 6: Subjects and average grades ===';
SELECT subject, AVG(grade) as average_grade
FROM grades
GROUP BY subject
ORDER BY average_grade DESC;

-- Query 7: Top 3 students by average grade
SELECT '=== Query 7: Top 3 students ===';
SELECT s.full_name, AVG(g.grade) as average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.full_name
ORDER BY average_grade DESC
LIMIT 3;

-- Query 8: Students with any grade below 80
SELECT '=== Query 8: Students with grades below 80 ===';
SELECT DISTINCT s.full_name, g.subject, g.grade
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE g.grade < 80
ORDER BY g.grade;

-- 4. PERFORMANCE OPTIMIZATION
-- ---------------------------
-- Create indexes to optimize frequent queries
CREATE INDEX IF NOT EXISTS idx_students_birth_year ON students(birth_year);
CREATE INDEX IF NOT EXISTS idx_grades_student_id ON grades(student_id);
CREATE INDEX IF NOT EXISTS idx_grades_subject ON grades(subject);
CREATE INDEX IF NOT EXISTS idx_grades_grade ON grades(grade);

SELECT '=== Database setup complete ===';