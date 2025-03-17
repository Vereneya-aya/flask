from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Настроим логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log_storage = []  # Храним логи в списке


@app.route('/log', methods=['POST'])
def log():
    """Принимает лог-сообщения через POST-запрос"""
    log_data = request.form.to_dict()
    log_storage.append(log_data)

    # Записываем лог в файл
    app.logger.info(f"Получен лог: {log_data}")

    return "OK", 200


@app.route('/logs', methods=['GET'])
def get_logs():
    """Возвращает все собранные логи"""
    return jsonify(log_storage)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3000, debug=True)