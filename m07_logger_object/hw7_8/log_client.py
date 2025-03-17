import logging
import logging.handlers

LOG_SERVER_HOST = "127.0.0.1"
LOG_SERVER_PORT = 3000
LOG_SERVER_URL = "/log"

# Создаем логгер
logger = logging.getLogger("ServiceLogger")
logger.setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Создаем обработчик для отправки логов через HTTP
http_handler = logging.handlers.HTTPHandler(
    host=f"{LOG_SERVER_HOST}:{LOG_SERVER_PORT}",
    url=LOG_SERVER_URL,
    method="POST"
)

# Добавляем обработчик
logger.addHandler(http_handler)

# Тестовые логи
logger.info("Service started successfully.")
logger.error("An error occurred in the service.")

# curl http://127.0.0.1:3000/logs