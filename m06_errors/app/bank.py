from flask import Flask, jsonify, render_template_string
import logging
import csv
from werkzeug.exceptions import InternalServerError

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BRANCH_CARDS_FILE = "fixtures/branch_cards.csv"


def get_person_name(person_id):
    """Ищет человека в файле CSV."""
    logger.debug(f"Ищем person_id={person_id} в файле {BRANCH_CARDS_FILE}")

    try:
        with open(BRANCH_CARDS_FILE, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for record in csv_reader:
                if int(record["id"]) == person_id:
                    logger.info(f"Найден person_id={person_id}: {record['name']}")
                    return record["name"]

        logger.warning(f"Person_id={person_id} не найден")
        raise ValueError("Person not found")  # Поднимаем ValueError, если не нашли

    except FileNotFoundError as e:
        logger.error("Файл с данными не найден")
        raise e

    except OSError as e:
        logger.error("Ошибка файловой системы")
        raise e

    except ValueError as e:
        raise e

    except Exception as e:
        logger.exception(f"Неизвестная ошибка: {e}")
        raise InternalServerError() from e

    # --- Обработчики ошибок ---


@app.errorhandler(FileNotFoundError)
def handle_file_not_found(e):
    logger.error("Файл с данными не найден")
    return jsonify({"error": "Файл с данными не найден"}), 500


@app.errorhandler(OSError)
def handle_os_error(e):
    logger.error("Ошибка файловой системы")
    return jsonify({"error": "Ошибка файловой системы"}), 500


@app.errorhandler(ValueError)
def handle_value_error(e):
    logger.warning("Человек не найден")
    return "error Человек не найден", 404


@app.errorhandler(InternalServerError)
def handle_internal_server_error(e):
    logger.error("Внутренняя ошибка сервера")
    return jsonify({"error": "Внутренняя ошибка сервера"}), 500


# --- Новый обработчик ошибки 404 ---
@app.errorhandler(404)
def page_not_found(e):
    """Выводит список доступных страниц при ошибке 404"""
    routes = [rule.rule for rule in app.url_map.iter_rules() if
              "GET" in rule.methods and not rule.rule.startswith("/static")]

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Страница не найдена</title>
    </head>
    <body>
        <h1>Ошибка 404: Страница не найдена</h1>
        <p>Возможно, вы имели в виду один из этих доступных маршрутов:</p>
        <ul>
            {% for route in routes %}
                <li><a href="{{ route }}">{{ route }}</a></li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """

    return render_template_string(html_template, routes=routes), 404


# --- Endpoint ---
@app.route('/person/<int:person_id>')
def person_lookup(person_id):
    name = get_person_name(person_id)
    return jsonify({"name": name})


# --- Запуск ---
if __name__ == '__main__':
    logger.info("Запуск Bank API")
    app.run(debug=True)