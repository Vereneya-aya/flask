"""
Иван Совин - эффективный менеджер.
Когда к нему приходит сотрудник просить повышение з/п -
    Иван может повысить её только на 10%.

Если после повышения з/п сотрудника будет больше з/п самого
    Ивана Совина - сотрудника увольняют, в противном случае з/п
    сотрудника повышают.

Давайте поможем Ивану стать ещё эффективнее,
    автоматизировав его нелёгкий труд.
    Пожалуйста реализуйте функцию которая по имени сотрудника
    либо повышает ему з/п, либо увольняет сотрудника
    (удаляет запись о нём из БД).

Таблица с данными называется `table_effective_manager`
"""
import sqlite3


def ivan_sovin_the_most_effective(c: sqlite3.Cursor, name: str) -> None:
    # Получаем зарплату Ивана Совина
    c.execute("""
        SELECT salary FROM table_effective_manager WHERE name = 'Иван Совин'
    """)
    result = c.fetchone()
    if result is None:
        raise ValueError("Иван Совин не найден в таблице")
    ivan_salary = result[0]

    # Получаем зарплату сотрудника
    c.execute("""
        SELECT salary FROM table_effective_manager WHERE name = ?
    """, (name,))
    result = c.fetchone()
    if result is None:
        # Сотрудника нет — ничего не делаем
        return

    employee_salary = result[0]
    new_salary = int(employee_salary * 1.1)

    if new_salary > ivan_salary:
        # Увольняем сотрудника
        c.execute("""
            DELETE FROM table_effective_manager WHERE name = ?
        """, (name,))
    else:
        # Повышаем зарплату
        c.execute("""
            UPDATE table_effective_manager
            SET salary = ?
            WHERE name = ?
        """, (new_salary, name))

    c.connection.commit()


with sqlite3.connect("hw.db") as conn:
    cursor = conn.cursor()
    ivan_sovin_the_most_effective(cursor, "Соловьёв Ж.Щ.")
