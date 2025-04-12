import sqlite3
'''
conn = sqlite3.connect("practise.db")
cursor = conn.cursor()

# Создаём таблицу, если её нет
cursor.execute("""
CREATE TABLE IF NOT EXISTS table_kotlin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    wind_speed REAL NOT NULL
);
""")

# Добавим тестовые данные
cursor.executemany("""
INSERT INTO table_kotlin (date, wind_speed) VALUES (?, ?)
""", [
    ("2024-01-01", 25.5),
    ("2024-01-02", 30.2),
    ("2024-01-03", 33.1),
    ("2024-01-04", 35.0),
    ("2024-01-05", 28.3),
    ("2024-01-06", 40.2),
    ("2024-01-07", 32.8)
])

conn.commit()
conn.close()
'''

def count_hurricane_days():
    conn = sqlite3.connect("practise.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM table_kotlin WHERE wind_speed >= 33")
    result = cursor.fetchone()[0]  # fetchone() вернёт кортеж, берем 1-й элемент

    conn.close()
    return result

# Вызываем функцию
print(f"Количество ураганных дней: {count_hurricane_days()}")