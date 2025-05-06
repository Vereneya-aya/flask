SELECT 
    t.name AS teacher_name,
    ROUND(AVG(g.grade), 2) AS avg_grade
FROM grades g
JOIN assignments a ON g.assignment_id = a.id
JOIN teachers t ON a.teacher_id = t.id
GROUP BY t.id
ORDER BY avg_grade ASC
LIMIT 1;

SELECT 
    s.name AS student_name,
    ROUND(AVG(g.grade), 2) AS avg_grade
FROM grades g
JOIN students s ON g.student_id = s.id
GROUP BY s.id
ORDER BY avg_grade DESC
LIMIT 10;

SELECT s.name
FROM students s
WHERE s.id IN (
    SELECT g.student_id
    FROM grades g
    JOIN assignments a ON g.assignment_id = a.id
    WHERE a.teacher_id = (
        SELECT a.teacher_id
        FROM grades g
        JOIN assignments a ON g.assignment_id = a.id
        GROUP BY a.teacher_id
        ORDER BY AVG(g.grade) DESC
        LIMIT 1
    )
);

SELECT DISTINCT s.name
FROM grades g
JOIN assignments a ON g.assignment_id = a.id
JOIN teachers t ON a.teacher_id = t.id
JOIN students s ON g.student_id = s.id
WHERE t.id = (
    SELECT a.teacher_id
    FROM grades g
    JOIN assignments a ON g.assignment_id = a.id
    GROUP BY a.teacher_id
    ORDER BY AVG(g.grade) DESC
    LIMIT 1
);

SELECT 
    c.name AS class_name,
    AVG(sub.deadline_missed_count) AS avg_missed,
    MAX(sub.deadline_missed_count) AS max_missed,
    MIN(sub.deadline_missed_count) AS min_missed
FROM (
    SELECT s.class_id, s.id AS student_id, COUNT(*) AS deadline_missed_count
    FROM grades g
    JOIN students s ON g.student_id = s.id
    WHERE g.deadline_missed = 1
    GROUP BY s.id
) sub
JOIN classes c ON sub.class_id = c.id
GROUP BY c.id;

SELECT 
    c.name AS class_name,
    COUNT(DISTINCT s.id) AS total_students,
    ROUND(AVG(g.grade), 2) AS avg_grade,
    SUM(CASE WHEN g.submitted = 0 THEN 1 ELSE 0 END) AS not_submitted_count,
    SUM(CASE WHEN g.deadline_missed = 1 THEN 1 ELSE 0 END) AS missed_deadline_count,
    SUM(CASE WHEN g.resubmitted = 1 THEN 1 ELSE 0 END) AS resubmissions
FROM grades g
JOIN students s ON g.student_id = s.id
JOIN classes c ON s.class_id = c.id
GROUP BY c.id;


SELECT 
    ROUND(AVG(g.grade), 2) AS avg_grade_for_read_tasks
FROM grades g
JOIN assignments a ON g.assignment_id = a.id
WHERE a.read_required = 1;