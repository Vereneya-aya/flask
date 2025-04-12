import sqlite3
'''
# Подключаемся к базе (если её нет, она создастся автоматически)
conn = sqlite3.connect("practise.db")
cursor = conn.cursor()
*//
# Создаём таблицу table_warehouse
cursor.execute("""
CREATE TABLE IF NOT EXISTS table_warehouse (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    amount INTEGER NOT NULL
);
""")

# Создаём таблицу book_list
cursor.execute("""
CREATE TABLE IF NOT EXISTS book_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER NOT NULL
);
""")

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()
'''

def add_10_records_to_table_warehouse(cursor: sqlite3.Cursor) -> None:
    products = [
        ("Яблоки", "Свежие красные яблоки", 50),
        ("Бананы", "Спелые бананы", 30),
        ("Апельсины", "Сочные апельсины", 40),
        ("Груши", "Сладкие груши", 25),
        ("Мандарины", "Без косточек", 35),
        ("Клубника", "Сладкая клубника", 20),
        ("Арбузы", "Большие арбузы", 10),
        ("Виноград", "Зелёный виноград", 15),
        ("Персики", "Спелые персики", 22),
        ("Сливы", "Фиолетовые сливы", 18)
    ]

    cursor.executemany("INSERT INTO table_warehouse (name, description, amount) VALUES (?, ?, ?)", products)

# Подключаемся к базе и вызываем функцию
conn = sqlite3.connect("practise.db")
cur = conn.cursor()

add_10_records_to_table_warehouse(cur)

conn.commit()
conn.close()