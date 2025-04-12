"""
Иногда бывает важно сгенерировать какие то табличные данные по заданным характеристикам.
К примеру, если вы будете работать тестировщиками, вам может потребоваться добавить
    в тестовую БД такой правдоподобный набор данных (покупки за сутки, набор товаров в магазине,
    распределение голосов в онлайн голосовании).

Давайте этим и займёмся!

Представим, что наша FrontEnd команда делает страницу сайта УЕФА с жеребьевкой команд
    по группам на чемпионате Европы.

Условия жеребьёвки такие:
Есть N групп.
В каждую группу попадает 1 "сильная" команда, 1 "слабая" команда и 2 "средние команды".

Задача: написать функцию generate_data, которая на вход принимает количество групп (от 4 до 16ти)
    и генерирует данные, которыми заполняет 2 таблицы:
        1. таблицу со списком команд (столбцы "номер команды", "Название", "страна", "сила команды")
        2. таблицу с результатами жеребьёвки (столбцы "номер команды", "номер группы")

Таблица с данными называется `uefa_commands` и `uefa_draw`
"""
import sqlite3

import random

# Для генерации случайных названий и стран
COMMAND_NAMES = [f"Команда {i}" for i in range(1, 65)]
COUNTRIES = ["Германия", "Франция", "Испания", "Италия", "Португалия", "Англия", "Нидерланды", "Бельгия"]

def generate_test_data(c: sqlite3.Cursor, number_of_groups: int) -> None:
    if not (4 <= number_of_groups <= 16):
        raise ValueError("Количество групп должно быть от 4 до 16")

    total_teams = number_of_groups * 4
    levels_distribution = (
        ['strong'] * number_of_groups +
        ['weak'] * number_of_groups +
        ['medium'] * (2 * number_of_groups)
    )

    random.shuffle(levels_distribution)
    team_data = []

    # Создаём команды
    for i in range(1, total_teams + 1):
        name = COMMAND_NAMES[i % len(COMMAND_NAMES)] + f" #{i}"
        country = random.choice(COUNTRIES)
        level = levels_distribution[i - 1]
        team_data.append((i, name, country, level))

    # Вставка команд в таблицу
    c.executemany(
        "INSERT INTO uefa_commands (command_number, command_name, command_country, command_level) VALUES (?, ?, ?, ?);",
        team_data
    )

    # Группировка по уровням
    strong = [team for team in team_data if team[3] == 'strong']
    weak = [team for team in team_data if team[3] == 'weak']
    medium = [team for team in team_data if team[3] == 'medium']

    draw_data = []

    for group_number in range(1, number_of_groups + 1):
        group_teams = [
            strong.pop(),
            weak.pop(),
            medium.pop(),
            medium.pop()
        ]
        for team in group_teams:
            command_number = team[0]
            draw_data.append((command_number, group_number))

    # Вставка результатов жеребьёвки
    c.executemany(
        "INSERT INTO uefa_draw (command_number, group_number) VALUES (?, ?);",
        draw_data
    )

    c.connection.commit()

with sqlite3.connect("hw.db") as conn:
    cursor = conn.cursor()
  # очистка и создание таблиц
    generate_test_data(cursor, number_of_groups=6)  # например, 6 групп