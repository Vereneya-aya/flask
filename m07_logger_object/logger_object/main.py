import logging
from flask import Flask
from http_utils import get_ip_address
from subprocess_utils import get_kernel_version

# === 1. Создаём логгер "main" ===
logger_main = logging.getLogger("main")
logger_main.setLevel(logging.INFO)

# === 2. Создаём общий логгер "utils" (родительский для http и subprocess) ===
logger_utils = logging.getLogger("utils")
logger_utils.setLevel(logging.DEBUG)

# === 3. Создаём обработчик (хэндлер) ===
file_handler = logging.FileHandler("app.log")  # Лог-файл
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(name)s || %(levelname)s || %(message)s || %(module)s.%(funcName)s:%(lineno)d"
)
file_handler.setFormatter(formatter)

# === 4. Добавляем обработчик к основным логгерам ===
logger_main.addHandler(file_handler)
logger_utils.addHandler(file_handler)

# === 5. Отключаем передачу логов utils в root (чтобы не дублировать) ===
logger_utils.propagate = False

app = Flask(__name__)

@app.route("/get_system_info")
def get_system_info():
    logger_main.info("start_working")
    ip_address = get_ip_address()
    kernel_version = get_kernel_version()
    return f"IP: {ip_address}, Kernel: {kernel_version}"

if __name__ == "__main__":
    app.run(debug=True)