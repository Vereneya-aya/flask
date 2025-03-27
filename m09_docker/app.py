import os
from flask import Flask, jsonify, make_response

app = Flask(__name__)

# Получаем имя сервиса из переменной окружения
SERVICE_NAME = os.environ.get("SERVICE_NAME", "Application")
ADMIN_NAME = os.environ.get("ADMIN_NAME", "Unknown Admin")  # Добавили имя админа

@app.route("/hello/<user>")
def hello_user(user):
    return make_response(jsonify({"message": f"Hello from {SERVICE_NAME}, {user}. Admin: {ADMIN_NAME}"}), 200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)