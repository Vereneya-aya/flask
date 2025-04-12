"""
Вы работаете программистом в IT отделе ГИБДД.
    Ваш отдел отвечает за обслуживание камер,
    которые фиксируют превышения скорости и выписывают автоматические штрафы.
За последний месяц к вам пришло больше тысячи жалоб на ошибочно назначенные штрафы,
    из которых около 100 были признаны и правда ошибочными.

Список из дат и номеров автомобилей ошибочных штрафов прилагается к заданию,
    пожалуйста удалите записи об этих штрафах из таблицы `table_fees`
"""

import sqlite3
import csv


def delete_wrong_fees(c: sqlite3.Cursor, wrong_fees_file: str) -> None:
    """
    Удаляет ошибочные штрафы из таблицы table_fees на основе данных из CSV-файла.
    """
    with open(wrong_fees_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Пропускаем заголовок

        wrong_fees = [(row[1], row[0]) for row in reader]  # Соотносим timestamp и truck_number

    query = "DELETE FROM table_fees WHERE timestamp = ? AND truck_number = ?"
    c.executemany(query, wrong_fees)


if __name__ == "__main__":
    with sqlite3.connect("hw.db") as conn:
        cursor = conn.cursor()
        delete_wrong_fees(cursor, "wrong_fees.csv")
        conn.commit()

