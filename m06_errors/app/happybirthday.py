import json
import logging
import os

from flask import Flask, jsonify

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("account_book")

# Пути к данным
current_dir = os.path.dirname(os.path.abspath(__file__))
fixtures_dir = os.path.join(current_dir, "fixtures")

# Отделы
departments = {"IT": "it_dept", "PROD": "production_dept"}

@app.route("/account/<department>/<int:account_number>/")
def sort_endpoint(department: str, account_number: int):
    logger.info(f"Получен запрос: department={department}, account_number={account_number}")

    # Проверяем существование отдела
    dept_directory_name = departments.get(department)
    if dept_directory_name is None:
        logger.warning(f"Отдел '{department}' не найден!")
        return jsonify({"error": "Department not found"}), 404

    # Формируем путь к файлу
    full_department_path = os.path.join(fixtures_dir, dept_directory_name)
    account_data_file = os.path.join(full_department_path, f"{account_number}.json")

    # Проверяем существование файла
    if not os.path.exists(account_data_file):
        logger.error(f"Файл {account_data_file} не найден!")
        return jsonify({"error": "Account data not found"}), 404

    try:
        # Читаем файл
        with open(account_data_file, "r", encoding="utf-8") as fi:
            account_data_json = json.load(fi)

        # Достаём данные
        name = account_data_json.get("name")
        birth_date = account_data_json.get("birth_date")

        if not name or not birth_date:
            logger.error(f"Ошибка в файле {account_data_file}: отсутствуют name или birth_date")
            return jsonify({"error": "Invalid data format"}), 400

        # Парсим дату
        try:
            day, month, _ = birth_date.split(".")
        except ValueError:
            logger.error(f"Некорректный формат даты в {account_data_file}: {birth_date}")
            return jsonify({"error": "Invalid date format"}), 400

        logger.info(f"Данные сотрудника: {name}, дата рождения: {day}.{month}")
        return jsonify({"name": name, "birth_date": f"{day}.{month}"})

    except json.JSONDecodeError:
        logger.error(f"Ошибка чтения JSON в файле {account_data_file}")
        return jsonify({"error": "Invalid JSON format"}), 400

    except Exception as e:
        logger.critical(f"Неизвестная ошибка: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    logger.info("Запуск сервера Flask для учёта сотрудников")
    app.run(debug=True)