from flask import Flask
import os
import re
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Глобальные переменные
cars_list = ["Chevrolet", "Renault", "Ford", "Lada"]
cats_list = ["корниш-рекс", "русская голубая", "шотландская вислоухая", "мейн-кун", "манчкин"]
counter_visits = 0
financial_storage = {}

@app.route("/max_number/<path:numbers>")
def max_number(numbers: str):
    try:
        number_list = [float(num) for num in numbers.split("/")]
        max_num = max(number_list)
        return f"Максимальное число: <i>{max_num}</i>"
    except ValueError:
        return "Ошибка: Переданы некорректные данные. Используйте только числа."

@app.route("/head_file/<int:size>/<path:relative_path>")
def head_file(size: int, relative_path: str):
    abs_path = os.path.abspath(relative_path)
    try:
        with open(abs_path, "r", encoding="utf-8") as file:
            result_text = file.read(size)
        result_size = len(result_text)
        return f"<b>{abs_path}</b> {result_size}<br>{result_text}"
    except FileNotFoundError:
        return "Ошибка: Файл не найден."
    except Exception as e:
        return f"Ошибка: {str(e)}"

@app.route("/add/<date>/<int:number>")
def add_expense(date: str, number: int):
    year, month = int(date[:4]), int(date[4:6])
    financial_storage.setdefault(year, {}).setdefault(month, 0)
    financial_storage[year][month] += number
    return f"Добавлено {number} руб. в {date}"

@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    total = sum(financial_storage.get(year, {}).values())
    return f"Общие расходы за {year} год: {total} руб."

@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    total = financial_storage.get(year, {}).get(month, 0)
    return f"Общие расходы за {month:02d}.{year} год: {total} руб."

@app.route("/hello_world")
def hello_world():
    return "Привет, мир!"

@app.route("/hello/<username>")
def hello_user(username):
    return f'Привет, {username}!'

@app.route("/even/<int:number>")
def even(number: int):
    res = 'odd' if number % 2 else 'even'
    return f'The number {number} is <b>{res}</b>'

@app.route("/compare/<float:num1>/<float:num2>")
def compare(num1: float, num2: float):
    if num1 > num2:
        result = f"{num1} больше, чем {num2}"
    elif num1 < num2:
        result = f"{num2} больше, чем {num1}"
    else:
        result = f"{num1} и {num2} равны"
    return f"<h3>{result}</h3>"

@app.route("/cars")
def cars():
    return ", ".join(cars_list)

@app.route("/cats")
def cats():
    return random.choice(cats_list)

@app.route("/get_time/now")
def get_time_now():
    current_time = datetime.now().strftime('%H:%M:%S')
    return f"Точное время: {current_time}"

@app.route("/get_time/future")
def get_time_future():
    future_time = (datetime.now() + timedelta(hours=1)).strftime('%H:%M:%S')
    return f"Точное время через час будет {future_time}"

@app.route("/counter")
def counter():
    global counter_visits
    counter_visits += 1
    return f"Страница /counter открыта {counter_visits} раз(а)"

WEEKDAYS = ("понедельника", "вторника", "среды", "четверга", "пятницы", "субботы", "воскресенья")

@app.route("/week/<name>")
def weekday(name: str):
    weekday = datetime.today().weekday()
    return f"Привет, {name}. Хорошей {WEEKDAYS[weekday]}!"

if __name__ == "__main__":
    app.run(debug=True)
