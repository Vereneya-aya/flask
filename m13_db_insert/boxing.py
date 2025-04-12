import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect("boxing.db")
cursor = conn.cursor()
'''
# Создаём таблицу с соперниками
cursor.execute("""
CREATE TABLE IF NOT EXISTS opponents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    defeated BOOLEAN NOT NULL
);
""")

# Добавляем список соперников (6 уже побеждено)
cursor.executemany("""
INSERT INTO opponents (name, defeated) VALUES (?, ?)
""", [
    ("Иван Драго", 1),
    ("Рокки Бальбоа", 0),
    ("Майк Тайсон", 1),
    ("Мохаммед Али", 0),
    ("Флойд Мейвезер", 1),
    ("Рой Джонс", 0),
    ("Сонни Листон", 1),
    ("Джо Фрейзер", 0),
    ("Оскар Де Ла Хойя", 1),
    ("Тайсон Фьюри", 0)
])

conn.commit()
conn.close()

def delete_defeated_opponents():
    with sqlite3.connect("boxing.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM opponents WHERE defeated = 1")

# Запускаем функцию
delete_defeated_opponents()
'''
def show_opponents():
    conn = sqlite3.connect("boxing.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM opponents")
    for row in cursor.fetchall():
        print(row)

    conn.close()

# Выводим список оставшихся соперников
show_opponents()