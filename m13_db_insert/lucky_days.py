import sqlite3
'''
conn = sqlite3.connect("practise.db")
cursor = conn.cursor()

# Создаём таблицу для отслеживания сбора мусора
cursor.execute("""
CREATE TABLE IF NOT EXISTS table_cleanup (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    month INTEGER NOT NULL,
    plastic_bags INTEGER NOT NULL,
    aluminum_bags INTEGER NOT NULL,
    recycled BOOLEAN NOT NULL
);
""")

# Добавим тестовые данные
cursor.executemany("""
INSERT INTO table_cleanup (date, month, plastic_bags, aluminum_bags, recycled) VALUES (?, ?, ?, ?, ?)
""", [
    ("2024-03-01", 3, 2, 1, 1),  # Очень удачный
    ("2024-03-02", 3, 3, 1, 0),  # Просто удачный
    ("2024-03-03", 3, 1, 0, 0),  # Неудачный
    ("2024-03-04", 3, 2, 1, 1),  # Очень удачный
    ("2024-03-05", 3, 2, 1, 0),  # Просто удачный
    ("2024-03-06", 3, 2, 1, 1),  # Очень удачный
    ("2024-03-07", 3, 3, 1, 1)   # Очень удачный
])

conn.commit()
conn.close()

'''

def calculate_lucky_days_percentage(month: int):
    conn = sqlite3.connect("practise.db")
    cursor = conn.cursor()

    # Подсчёт всех дней в месяце
    cursor.execute("SELECT COUNT(*) FROM table_cleanup WHERE month = ?", (month,))
    total_days = cursor.fetchone()[0]

    # Подсчёт очень удачных дней
    cursor.execute("""
        SELECT COUNT(*) FROM table_cleanup 
        WHERE month = ? AND plastic_bags >= 2 AND aluminum_bags >= 1 AND recycled = 1
    """, (month,))
    lucky_days = cursor.fetchone()[0]

    conn.close()

    # Если нет данных, возвращаем 0%
    if total_days == 0:
        return 0

    return (lucky_days / total_days) * 100

# Пример использования
month = 3  # Март
print(f"Процент очень удачных дней в {month}-м месяце: {calculate_lucky_days_percentage(month):.2f}%")