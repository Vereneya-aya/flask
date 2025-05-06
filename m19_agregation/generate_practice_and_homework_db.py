import sqlite3
import random

# Создаем подключение и курсор
conn = sqlite3.connect("school_homework.db")
cur = conn.cursor()

# Удалим таблицы, если они уже есть
tables = ['teachers', 'students', 'classes', 'assignments', 'grades']
for table in tables:
    cur.execute(f"DROP TABLE IF EXISTS {table}")

# Таблицы
cur.execute("""
CREATE TABLE teachers (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

cur.execute("""
CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

cur.execute("""
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    class_id INTEGER,
    FOREIGN KEY (class_id) REFERENCES classes (id)
)
""")

cur.execute("""
CREATE TABLE assignments (
    id INTEGER PRIMARY KEY,
    title TEXT,
    teacher_id INTEGER,
    read_required BOOLEAN,
    deadline_passed BOOLEAN,
    FOREIGN KEY (teacher_id) REFERENCES teachers (id)
)
""")

cur.execute("""
CREATE TABLE grades (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    assignment_id INTEGER,
    grade INTEGER, -- 1 to 5
    submitted BOOLEAN,
    resubmitted BOOLEAN,
    deadline_missed BOOLEAN,
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (assignment_id) REFERENCES assignments (id)
)
""")

# Примерные данные
teachers = ["Иванов", "Петров", "Сидорова", "Кузнецова", "Орлова"]
classes = ["10А", "10Б", "11А", "11Б"]

# Вставляем преподавателей и классы
cur.executemany("INSERT INTO teachers (name) VALUES (?)", [(t,) for t in teachers])
cur.executemany("INSERT INTO classes (name) VALUES (?)", [(c,) for c in classes])

# Получим ID
cur.execute("SELECT id FROM teachers")
teacher_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT id FROM classes")
class_ids = [row[0] for row in cur.fetchall()]

# Добавим учеников
student_names = [f"Ученик{i}" for i in range(1, 41)]
students = [(name, random.choice(class_ids)) for name in student_names]
cur.executemany("INSERT INTO students (name, class_id) VALUES (?, ?)", students)

# Добавим задания
assignments = []
for i in range(1, 21):
    title = f"Задание {i}"
    teacher_id = random.choice(teacher_ids)
    read_required = random.choice([True, False])
    deadline_passed = random.choice([True, False])
    assignments.append((title, teacher_id, read_required, deadline_passed))

cur.executemany("INSERT INTO assignments (title, teacher_id, read_required, deadline_passed) VALUES (?, ?, ?, ?)", assignments)

# Добавим оценки
cur.execute("SELECT id FROM students")
student_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT id FROM assignments")
assignment_ids = [row[0] for row in cur.fetchall()]

grades = []
for student_id in student_ids:
    for assignment_id in random.sample(assignment_ids, 5):
        grade = random.randint(2, 5)
        submitted = random.choice([True, False])
        resubmitted = random.choice([True, False])
        deadline_missed = random.choice([True, False])
        grades.append((student_id, assignment_id, grade, submitted, resubmitted, deadline_missed))

cur.executemany("""
INSERT INTO grades (student_id, assignment_id, grade, submitted, resubmitted, deadline_missed)
VALUES (?, ?, ?, ?, ?, ?)""", grades)

conn.commit()
conn.close()
print("База данных успешно создана: school_homework.db")