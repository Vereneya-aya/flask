import sqlite3

DB_NAME = "movies.db"

def insert_data():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Добавим актеров
        cursor.execute("INSERT INTO actors (act_id, act_first_name, act_last_name, act_gender) VALUES (1, 'Tom', 'Hanks', 'M');")
        cursor.execute("INSERT INTO actors (act_id, act_first_name, act_last_name, act_gender) VALUES (2, 'Emma', 'Watson', 'F');")

        # Добавим фильмы
        cursor.execute("INSERT INTO movie (mov_id, mov_title) VALUES (1, 'Forrest Gump');")
        cursor.execute("INSERT INTO movie (mov_id, mov_title) VALUES (2, 'Harry Potter');")

        # Добавим режиссера
        cursor.execute("INSERT INTO director (dir_id, dir_first_name, dir_last_name) VALUES (1, 'Robert', 'Zemeckis');")

        # Добавим связи актеров с фильмами (каст)
        cursor.execute("INSERT INTO movie_cast (act_id, mov_id, role) VALUES (1, 1, 'Forrest');")
        cursor.execute("INSERT INTO movie_cast (act_id, mov_id, role) VALUES (2, 2, 'Hermione');")

        # Добавим связь фильма и режиссера
        cursor.execute("INSERT INTO movie_direction (dir_id, mov_id) VALUES (1, 1);")

        # Добавим оскара
        cursor.execute("INSERT INTO oscar_awarded (award_id, mov_id) VALUES (1, 1);")

        conn.commit()
        print("Данные успешно вставлены!")

if __name__ == "__main__":
    insert_data()