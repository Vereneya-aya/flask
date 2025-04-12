"""
Пожалуйста, запустите скрипт generate_hw_database.py прежде, чем приступать к выполнению практической работы. После выполнения скрипта у вас должен появиться файл базы hw.db и в нем таблица table_truck_with_vaccine
Грузовик перевозит очень важную вакцину.

Условия хранения этой вакцины весьма необычные -- в отсеке должна быть температура  18±2 градуса.
    Если температурный режим был нарушен - вакцина считается испорченной.

Для проверки состояния вакцины применяется датчик, который раз в час измеряет температуру внутри контейнера.
    Если в контейнере было хотя бы 3 часа с температурой, которая находится вне указанного выше диапазона -
    температурный режим считается нарушенным.

Пожалуйста, реализуйте функцию `check_if_vaccine_has_spoiled`,
    которая по номеру грузовика определяет, не испортилась ли вакцина.
"""
import sqlite3
from datetime import datetime, timedelta


def check_if_vaccine_has_spoiled(c: sqlite3.Cursor, truck_number: str) -> bool:
    # 1. Получаем все записи для указанного грузовика, отсортированные по времени
    c.execute(
        """
        SELECT timestamp, temperature_in_celsius
        FROM table_truck_with_vaccine
        WHERE LOWER(truck_number) = LOWER(?)
        ORDER BY timestamp
        """,
        (truck_number,)
    )

    records = c.fetchall()

    if not records:
        return False  # Если данных по грузовику нет, считаем, что всё в порядке

    # 2. Ищем нарушения температурного режима
    violation_time = timedelta(hours=0)  # Время нарушения
    prev_time = None  # Предыдущее время для проверки подряд идущих нарушений

    for timestamp, temperature in records:
        # Парсим timestamp в datetime
        current_time = datetime.fromisoformat(timestamp)

        # Проверяем, нарушена ли температура
        if not (16 <= temperature <= 20):
            if prev_time and (current_time - prev_time == timedelta(hours=1)):
                violation_time += timedelta(hours=1)  # Добавляем 1 час подряд
            else:
                violation_time = timedelta(hours=1)  # Начинаем отсчёт заново

            if violation_time >= timedelta(hours=3):
                return True  # Если 3 часа подряд нарушения, вакцина испорчена
        else:
            violation_time = timedelta(hours=0)  # Сбрасываем счётчик

        prev_time = current_time  # Обновляем предыдущее время

    return False  # Если не нашли 3 часа подряд нарушений, значит, вакцина не испорчена

with sqlite3.connect("hw.db") as conn:
    cursor = conn.cursor()
    truck_number = "а123вс77"  # Например, проверяем этот грузовик
    result = check_if_vaccine_has_spoiled(cursor, truck_number)
    print("Вакцина испорчена" if result else "Всё в порядке")