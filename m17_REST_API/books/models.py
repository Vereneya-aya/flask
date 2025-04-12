# models.py
import sqlite3

def get_connection():
    return sqlite3.connect("authors.db")

def get_all_authors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM authors")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1]} for r in rows]

def get_author(author_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM authors WHERE id = ?", (author_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1]}
    return None

def get_books_by_author(author_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM books WHERE author_id = ?", (author_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1]} for r in rows]

def get_book(author_id, book_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM books WHERE author_id = ? AND id = ?", (author_id, book_id))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "title": row[1]}
    return None

# models.py (добавь в конец)
def add_book(author_id, title):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author_id) VALUES (?, ?)", (title, author_id))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, "title": title}