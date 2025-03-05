from flask import Flask

app = Flask(__name__)

@app.route("/max_number/<path:numbers>")
def max_number(numbers: str):
    try:
        number_list = [float(num) for num in numbers.split("/")]
        return {"max_number": max(number_list)}
    except ValueError:
        return {"error": "Некорректные данные. Используйте только числа."}, 400