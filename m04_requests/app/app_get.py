from flask import Flask, request, jsonify
from datetime import datetime
from itertools import product

app = Flask(__name__)


def validate_date(date_str):
    try:
        date = datetime.strptime(date_str, "%Y%m%d")
        if date > datetime.now():
            return False
        return date
    except ValueError:
        return False


def validate_parameters(cell_tower_id, protocol, phone_prefix):
    if cell_tower_id <= 0:
        return "cell_tower_id должен быть больше 0"
    if protocol not in ["2G", "3G", "4G"]:
        return "protocol может быть только 2G, 3G или 4G"
    if not phone_prefix[:-1].isdigit() or len(phone_prefix) > 10 or not phone_prefix.endswith("*"):
        return "phone_prefix должен состоять из чисел, заканчиваться * и содержать не более 10 цифр"
    return None


@app.route("/validate", methods=["GET"])
def validate():
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    cell_tower_id = request.args.get("cell_tower_id", type=int, default=0)
    protocol = request.args.get("protocol")
    phone_prefix = request.args.get("phone_prefix")

    if date_from:
        date_from = validate_date(date_from)
        if not date_from:
            return "Ошибка: некорректная дата_from", 400

    if date_to:
        date_to = validate_date(date_to)
        if not date_to:
            return "Ошибка: некорректная дата_to", 400

    if date_from and date_to and date_from > date_to:
        return "Ошибка: date_to должно быть больше date_from", 400

    error_message = validate_parameters(cell_tower_id, protocol, phone_prefix)
    if error_message:
        return error_message, 400

    return "Все параметры корректны"
# http://127.0.0.1:5000/validate?date_from=20240301&date_to=20240302&cell_tower_id=1&protocol=4G&phone_prefix=12345*
# http://127.0.0.1:5000/validate?date_from=20240301&date_to=20240302&cell_tower_id=1&protocol=4G&phone_prefix=12345*

@app.route("/sum_product", methods=["GET"])
def sum_product():
    numbers = request.args.getlist("numbers", type=int)
    if not numbers:
        return "Ошибка: передайте числа в параметре numbers", 400
    return jsonify({"sum": sum(numbers), "product": eval("*".join(map(str, numbers)))})
# http://127.0.0.1:5000/sum_product?numbers=2&numbers=3&numbers=4

@app.route("/combinations", methods=["GET"])
def combinations():
    A = request.args.getlist("A", type=int)
    B = request.args.getlist("B", type=int)
    if not A or not B:
        return "Ошибка: передайте массивы A и B", 400
    return jsonify(list(product(A, B)))
# http://127.0.0.1:5000/combinations?A=1&A=2&A=3&B=4&B=5

@app.route("/closest_number", methods=["GET"])
def closest_number():
    A = request.args.getlist("A", type=int)
    X = request.args.get("X", type=int)
    if not A or X is None:
        return "Ошибка: передайте массив A и число X", 400
    return jsonify(min(A, key=lambda num: abs(num - X)))
# http://127.0.0.1:5000/closest_number?A=10&A=20&A=30&A=40&X=25

if __name__ == "__main__":
    app.run(debug=True)
