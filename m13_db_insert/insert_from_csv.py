import sqlite3
import csv


def insert_books_from_csv(cursor: sqlite3.Cursor, filename: str) -> None:
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        books = [row for row in reader]

    cursor.executemany("INSERT INTO book_list (title, author, year) VALUES (?, ?, ?)", books)


# Подключаемся к базе и вызываем функцию
conn = sqlite3.connect("practise.db")
cur = conn.cursor()

insert_books_from_csv(cur, "book_list.csv")

conn.commit()
conn.close()