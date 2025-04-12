# Задача 1: «Звёздные войны 2»
#
# Нам нужно скачать 20 персонажей из базы данных о Star Wars и записать их в БД. Реализуем две версии: с потоками и процессами.
#
# Сначала разберёмся, почему тут лучше использовать потоки, а не процессы:
# 	•	Запросы в сеть (HTTP) — это типичная I/O-bound задача, так как основное время программа тратит на ожидание ответа от сервера.
# 	•	Потоки хороши для этого, потому что не блокируют Python GIL, а переключаются между задачами во время ожидания данных.
# 	•	Процессы для такой задачи использовать неэффективно, так как каждый процесс создаёт свою копию памяти, что замедляет работу и потребляет больше ресурсов.

import requests
import sqlite3
import time
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor

API_URL = "https://swapi.dev/api/people/"
DB_NAME = "star_wars.db"


def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY,
        name TEXT,
        birth_year TEXT,
        gender TEXT
    )
    """)
    conn.commit()
    conn.close()


def fetch_character(id):
    response = requests.get(f"{API_URL}{id}/")
    if response.status_code == 200:
        data = response.json()
        return data["name"], data["birth_year"], data["gender"]
    return None


def save_to_db(character):
    if character:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO characters (name, birth_year, gender) VALUES (?, ?, ?)", character)
        conn.commit()
        conn.close()


def fetch_with_threads():
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_character, range(1, 21)))
    for character in results:
        save_to_db(character)


def fetch_with_processes():
    with Pool(processes=10) as pool:
        results = pool.map(fetch_character, range(1, 21))
    for character in results:
        save_to_db(character)


if __name__ == "__main__":
    create_db()

    start = time.time()
    fetch_with_threads()
    print(f"Threads execution time: {time.time() - start:.2f} sec")

    start = time.time()
    fetch_with_processes()
    print(f"Processes execution time: {time.time() - start:.2f} sec")
