# create_db.py
import sqlite3

conn = sqlite3.connect("authors.db")
cursor = conn.cursor()

# Удалим, если есть
cursor.execute("DROP TABLE IF EXISTS books")
cursor.execute("DROP TABLE IF EXISTS authors")

# Таблица авторов
cursor.execute("""
CREATE TABLE authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

# Таблица книг
cursor.execute("""
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES authors(id)
)
""")

# Вставим данные
cursor.execute("INSERT INTO authors (name) VALUES ('Лев Толстой')")
cursor.execute("INSERT INTO authors (name) VALUES ('Фёдор Достоевский')")

cursor.execute("INSERT INTO books (title, author_id) VALUES ('Война и мир', 1)")
cursor.execute("INSERT INTO books (title, author_id) VALUES ('Анна Каренина', 1)")
cursor.execute("INSERT INTO books (title, author_id) VALUES ('Преступление и наказание', 2)")
cursor.execute("INSERT INTO books (title, author_id) VALUES ('Идиот', 2)")

conn.commit()
conn.close()