from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/process_array", methods=["POST"])
def process_array():
    data = request.get_json()  # Получаем JSON-данные из запроса
    if not data or "numbers" not in data:
        return jsonify({"error": "Передайте массив чисел в формате JSON"}), 400

    numbers = data["numbers"]
    if not all(isinstance(num, (int, float)) for num in numbers):
        return jsonify({"error": "Массив должен содержать только числа"}), 400

    return jsonify({"sum": sum(numbers), "product": eval("*".join(map(str, numbers)))})

if __name__ == "__main__":
    app.run(debug=True)


    # http://127.0.0.1:5000/process_array