import sqlite3

DB_NAME = "movies.db"

# SQL-запросы на создание таблиц
CREATE_ACTORS_TABLE = """
CREATE TABLE IF NOT EXISTS actors (
    act_id INTEGER PRIMARY KEY,
    act_first_name VARCHAR(50),
    act_last_name VARCHAR(50),
    act_gender VARCHAR(1)
);
"""

CREATE_MOVIE_TABLE = """
CREATE TABLE IF NOT EXISTS movie (
    mov_id INTEGER PRIMARY KEY,
    mov_title VARCHAR(50)
);
"""

CREATE_DIRECTOR_TABLE = """
CREATE TABLE IF NOT EXISTS director (
    dir_id INTEGER PRIMARY KEY,
    dir_first_name VARCHAR(50),
    dir_last_name VARCHAR(50)
);
"""

CREATE_MOVIE_CAST_TABLE = """
CREATE TABLE IF NOT EXISTS movie_cast (
    act_id INTEGER,
    mov_id INTEGER,
    role VARCHAR(50),
    FOREIGN KEY (act_id) REFERENCES actors(act_id),
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id)
);
"""

CREATE_MOVIE_DIRECTION_TABLE = """
CREATE TABLE IF NOT EXISTS movie_direction (
    dir_id INTEGER,
    mov_id INTEGER,
    FOREIGN KEY (dir_id) REFERENCES director(dir_id),
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id)
);
"""

CREATE_OSCAR_AWARDED_TABLE = """
CREATE TABLE IF NOT EXISTS oscar_awarded (
    award_id INTEGER PRIMARY KEY,
    mov_id INTEGER,
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id)
);
"""

def create_tables():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.executescript(
            CREATE_ACTORS_TABLE +
            CREATE_MOVIE_TABLE +
            CREATE_DIRECTOR_TABLE +
            CREATE_MOVIE_CAST_TABLE +
            CREATE_MOVIE_DIRECTION_TABLE +
            CREATE_OSCAR_AWARDED_TABLE
        )
        print("Таблицы успешно созданы!")

if __name__ == "__main__":
    create_tables()