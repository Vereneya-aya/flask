import sqlite3

conn = sqlite3.connect("example.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    username TEXT PRIMARY KEY,
    email TEXT,
    first_name TEXT
);

CREATE TABLE post (
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT,
    content TEXT,
    FOREIGN KEY(author) REFERENCES user(username)
);
""")

# Вставляем пользователей
cursor.execute("INSERT INTO user (username, email, first_name) VALUES (?, ?, ?)",
               ("alice", "alice@example.com", "Alice"))
cursor.execute("INSERT INTO user (username, email, first_name) VALUES (?, ?, ?)",
               ("bob", "bob@example.com", "Bob"))

# Вставляем посты (автором указываем username)
cursor.execute("INSERT INTO post (author, content) VALUES (?, ?)",
               ("alice", "Привет от Алисы!"))
cursor.execute("INSERT INTO post (author, content) VALUES (?, ?)",
               ("bob", "Привет от Боба!"))

conn.commit()
conn.close()

