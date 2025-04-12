import sqlite3

conn = sqlite3.connect("example_surrogate.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    first_name TEXT
);

CREATE TABLE post (
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER,
    content TEXT,
    FOREIGN KEY(author_id) REFERENCES user(user_id)
);
""")
# Вставляем пользователей
cursor.execute("INSERT INTO user (username, email, first_name) VALUES (?, ?, ?)",
               ("alice", "alice@example.com", "Alice"))
cursor.execute("INSERT INTO user (username, email, first_name) VALUES (?, ?, ?)",
               ("bob", "bob@example.com", "Bob"))

# Получаем ID пользователей
cursor.execute("SELECT user_id FROM user WHERE username = ?", ("alice",))
alice_id = cursor.fetchone()[0]

cursor.execute("SELECT user_id FROM user WHERE username = ?", ("bob",))
bob_id = cursor.fetchone()[0]

# Вставляем посты
cursor.execute("INSERT INTO post (author_id, content) VALUES (?, ?)",
               (alice_id, "Привет от Алисы!"))
cursor.execute("INSERT INTO post (author_id, content) VALUES (?, ?)",
               (bob_id, "Привет от Боба!"))

conn.commit()
conn.close()