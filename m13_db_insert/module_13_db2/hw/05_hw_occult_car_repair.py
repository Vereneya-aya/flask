"""
В 20NN году оккультному автосалону "Чёртово колесо" исполняется ровно 13 лет.
    В честь этого они предлагает своим клиентам уникальную акцию:
    если вы обращаетесь в автосалон в пятницу тринадцатое и ваш автомобиль
    чёрного цвета и марки "Лада" или "BMW", то вы можете поменять колёса со скидкой 13%.
Младший менеджер "Чёртова колеса" слил данные клиентов в интернет,
    поэтому мы можем посчитать, как много клиентов автосалона могли воспользоваться
    скидкой (если бы они об этом знали). Давайте сделаем это!

Реализуйте функцию, c именем get_number_of_luckers, которая принимает на вход курсор и номер месяца,
    и в ответ возвращает число клиентов, которые могли бы воспользоваться скидкой автосалона.
    Таблица с данными называется `table_occult_car_repair`
"""
import sqlite3


def get_number_of_luckers(c: sqlite3.Cursor, month: int) -> int:
    query = """
        SELECT COUNT(*)
        FROM table_occult_car_repair
        WHERE
            strftime('%m', timestamp) = :month
            AND strftime('%w', timestamp) = '5'  -- пятница
            AND strftime('%d', timestamp) = '13'
            AND LOWER(car_colour) = 'чёрный'
            AND LOWER(car_type) IN ('лада', 'bmw')
    """

    # приводим месяц к строке формата '01', '02', ...
    formatted_month = f"{month:02d}"

    c.execute(query, {"month": formatted_month})
    (count,) = c.fetchone()
    return count

with sqlite3.connect("hw.db") as conn:
    cursor = conn.cursor()
    result = get_number_of_luckers(cursor, 3)  # например, март
    print(f"Клиентов, подходящих под акцию в марте: {result}")