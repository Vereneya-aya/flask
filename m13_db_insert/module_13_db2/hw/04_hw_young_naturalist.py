"""
Юный натуралист Петя решил посетить Юнтоловский заказник на рассвете и записать журнал всех птиц,
    которых он увидел в заказнике. Он написал программу, но, в процессе написания,
    так устал, что уснул на клавиатуре, отчего пол-программы стёрлось.

Наш юный натуралист точно помнит, что программа позволяла добавить в БД новую птицу и говорила ему,
    видел ли он такую птицу раньше.

Помогите восстановить исходный код программы ЮНат v0.1 ,
    реализовав функции log_bird (добавление новой птицы в БД) и check_if_such_bird_already_seen
    (проверка что мы уже видели такую птицу)

Пожалуйста помогите ему, реализовав функцию log_bird .
    При реализации не забудьте про параметризацию SQL запроса!
"""

import datetime
import sqlite3


def log_bird(
        c: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
        bird_count: int
) -> None:
    # Создание таблицы, если её ещё нет
    c.execute("""
        CREATE TABLE IF NOT EXISTS birds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL COLLATE NOCASE,
            count INTEGER NOT NULL,
            last_seen_at TEXT NOT NULL
        )
    """)

    # Проверяем, есть ли такая птица уже в БД (без учёта регистра)
    c.execute("SELECT id, count FROM birds WHERE name = ?", (bird_name,))
    result = c.fetchone()

    if result:
        bird_id, existing_count = result
        new_count = existing_count + bird_count
        c.execute("""
            UPDATE birds
            SET count = ?, last_seen_at = ?
            WHERE id = ?
        """, (new_count, date_time, bird_id))
        print("Такую птицу мы уже наблюдали! Информация обновлена.")
    else:
        c.execute("""
            INSERT INTO birds (name, count, last_seen_at)
            VALUES (?, ?, ?)
        """, (bird_name, bird_count, date_time))
        print("Добавлено новое наблюдение.")


def show_all_birds(c: sqlite3.Cursor) -> None:
    c.execute("SELECT name, count, last_seen_at FROM birds ORDER BY name COLLATE NOCASE")
    birds = c.fetchall()
    if birds:
        print("\nЖурнал наблюдений:")
        for name, count, last_seen in birds:
            print(f"• {name}: {count} раз(а), последнее наблюдение — {last_seen}")
    else:
        print("Наблюдений пока нет.")


if __name__ == "__main__":
    from datetime import datetime, timezone
    print("Программа помощи ЮНатам v0.1")

    name = input("Пожалуйста введите имя птицы\n> ").strip()
    count_str = input("Сколько птиц вы увидели?\n> ").strip()

    try:
        count = int(count_str)
    except ValueError:
        print("Пожалуйста, введите корректное число.")
        exit(1)

    right_now = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect("hw.db") as connection:
        cursor = connection.cursor()
        log_bird(cursor, name, right_now, count)
        show_all_birds(cursor)
