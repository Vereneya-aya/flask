import requests
import sqlite3
import threading
import time

API_URL = "https://swapi.dev/api/people/"
DB_NAME = "star_wars.db"


# Создание БД и таблицы
def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS characters (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        gender TEXT,
                        birth_year TEXT)''')
    conn.commit()
    conn.close()


# Функция для сохранения персонажа в БД
def save_to_db(name, gender, birth_year):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO characters (name, gender, birth_year) VALUES (?, ?, ?)", (name, gender, birth_year))
    conn.commit()
    conn.close()


# Последовательное выполнение
def fetch_characters_sequentially():
    start_time = time.time()
    for i in range(1, 21):
        response = requests.get(f"{API_URL}{i}/")
        if response.status_code == 200:
            data = response.json()
            save_to_db(data["name"], data["gender"], data["birth_year"])
    print(f"Sequential execution time: {time.time() - start_time:.2f} seconds")


# Функция для загрузки данных в потоке
def fetch_character_thread(i):
    response = requests.get(f"{API_URL}{i}/")
    if response.status_code == 200:
        data = response.json()
        save_to_db(data["name"], data["gender"], data["birth_year"])


# Параллельное выполнение
def fetch_characters_parallel():
    start_time = time.time()
    threads = []
    for i in range(1, 21):
        thread = threading.Thread(target=fetch_character_thread, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Parallel execution time: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    setup_database()
    print("Fetching characters sequentially...")
    fetch_characters_sequentially()
    print("Fetching characters in parallel...")
    fetch_characters_parallel()
