import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect("post_office.db")
cursor = conn.cursor()
'''
# Создаём таблицу с почтовыми отправлениями
cursor.execute("""
CREATE TABLE IF NOT EXISTS mail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient TEXT NOT NULL,
    month INTEGER NOT NULL
);
""")

# Добавляем тестовые данные (отправления за май и другие месяцы)
cursor.executemany("""
INSERT INTO mail (recipient, month) VALUES (?, ?)
""", [
    ("Иван Петров", 5),
    ("Мария Иванова", 5),
    ("Сергей Смирнов", 4),
    ("Анна Васильева", 5),
    ("Николай Сидоров", 6),
    ("Алексей Фёдоров", 5),
    ("Елена Кузнецова", 3),
])

conn.commit()
conn.close()


def update_may_to_june():
    with sqlite3.connect("post_office.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE mail SET month = 6 WHERE month = 5")

# Запускаем функцию
update_may_to_june()

'''
def show_mail():
    conn = sqlite3.connect("post_office.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM mail")
    for row in cursor.fetchall():
        print(row)

    conn.close()

# Выводим список всех отправлений
show_mail()