import sqlite3
import os

# Убедимся, что директория 'instance' существует
os.makedirs("instance", exist_ok=True)

conn = sqlite3.connect("instance/books.db")
cursor = conn.cursor()

# Удалим, если есть
cursor.execute("DROP TABLE IF EXISTS books")
cursor.execute("DROP TABLE IF EXISTS authors")

# Таблица авторов (разбиваем имя на части)
cursor.execute("""
CREATE TABLE authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT
)
""")

# Таблица книг
cursor.execute("""
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    year INTEGER,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors(id)
)
""")

# Вставим авторов
cursor.execute("""
INSERT INTO authors (first_name, last_name, middle_name) VALUES 
('Лев', 'Толстой', 'Николаевич')
""")

cursor.execute("""
INSERT INTO authors (first_name, last_name, middle_name) VALUES 
('Фёдор', 'Достоевский', 'Михайлович')
""")

# Вставим книги
cursor.execute("""
INSERT INTO books (title, year, author_id) VALUES 
('Война и мир', 1869, 1),
('Анна Каренина', 1877, 1),
('Преступление и наказание', 1866, 2),
('Идиот', 1869, 2)
""")

conn.commit()
conn.close()