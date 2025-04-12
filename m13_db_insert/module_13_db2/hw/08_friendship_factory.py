"""
На заводе "Дружба" работает очень дружный коллектив.
Рабочие работают посменно, в смене -- 10 человек.
На смену заходит 366 .

Бухгалтер завода составила расписание смен и занесла его в базу данных
    в таблицу `table_work_schedule`, но совершенно не учла тот факт,
    что все сотрудники люди спортивные и ходят на различные спортивные кружки:
        1. футбол (проходит по понедельникам)
        2. хоккей (по вторникам
        3. шахматы (среды)
        4. SUP сёрфинг (четверг)
        5. бокс (пятница)
        6. Dota2 (суббота)
        7. шах-бокс (воскресенье)

Как вы видите, тренировки по этим видам спорта проходят в определённый день недели.

Пожалуйста помогите изменить расписание смен с учётом личных предпочтений коллектива
    (или докажите, что то, чего они хотят - не возможно).
"""
import sqlite3
import datetime

def update_work_schedule(c: sqlite3.Cursor) -> None:
    # Сопоставим спорт и день недели
    sport_days = {
        "футбол": 0,
        "хоккей": 1,
        "шахматы": 2,
        "SUP сёрфинг": 3,
        "бокс": 4,
        "Dota2": 5,
        "шах-бокс": 6
    }

    # Получим предпочтения всех сотрудников
    c.execute("SELECT id, preferable_sport FROM table_friendship_employees")
    employee_sport = dict(c.fetchall())  # id -> sport

    # Преобразуем в id -> запрещённый день
    unavailable_day = {eid: sport_days[sport] for eid, sport in employee_sport.items()}

    # Получим все даты из расписания
    c.execute("SELECT DISTINCT date FROM table_friendship_schedule")
    all_dates = [row[0] for row in c.fetchall()]

    for date in all_dates:
        weekday = datetime.datetime.strptime(date, "%Y-%m-%d").weekday()

        # Получаем всех работников в эту дату
        c.execute("""
            SELECT employee_id FROM table_friendship_schedule
            WHERE date = ?
        """, (date,))
        employees_today = [row[0] for row in c.fetchall()]

        # Выделим тех, у кого сегодня спорт
        conflicted = [eid for eid in employees_today if unavailable_day.get(eid) == weekday]

        # Попробуем решить конфликты
        for eid in conflicted:
            # Найдём подходящего человека, с кем можно поменяться
            for potential_swap in range(1, 367):
                if potential_swap in employees_today:
                    continue  # уже на смене
                if unavailable_day.get(potential_swap) == weekday:
                    continue  # у него тоже спорт

                # Есть ли день, когда потенциальный сотрудник работал, а конфликтный нет?
                c.execute("""
                    SELECT date FROM table_friendship_schedule
                    WHERE employee_id = ?
                """, (potential_swap,))
                potential_dates = [row[0] for row in c.fetchall()]

                swap_date = None
                for d in potential_dates:
                    wd = datetime.datetime.strptime(d, "%Y-%m-%d").weekday()
                    if unavailable_day.get(eid) != wd and unavailable_day.get(potential_swap) != weekday:
                        swap_date = d
                        break

                if swap_date:
                    # Удаляем обе записи
                    c.execute("""
                        DELETE FROM table_friendship_schedule
                        WHERE employee_id = ? AND date = ?
                    """, (eid, date))
                    c.execute("""
                        DELETE FROM table_friendship_schedule
                        WHERE employee_id = ? AND date = ?
                    """, (potential_swap, swap_date))

                    # Вставляем поменявшись
                    c.execute("""
                        INSERT INTO table_friendship_schedule (employee_id, date) VALUES (?, ?)
                    """, (eid, swap_date))
                    c.execute("""
                        INSERT INTO table_friendship_schedule (employee_id, date) VALUES (?, ?)
                    """, (potential_swap, date))
                    break

    c.connection.commit()
