import logging
import sys
import logging.config
from logging_config import LOGGING_CONFIG

def configure_logging():
    """Применяет dict-конфигурацию логирования."""
    logging.config.dictConfig(LOGGING_CONFIG)

# def configure_logging():
#     """Настраивает логирование с выводом в stdout и записью в разные файлы по уровням."""
#
#     # Удаляем старые обработчики, если они уже есть
#     root_logger = logging.getLogger()
#     root_logger.handlers = []
#
#     # Формат логов
#     formatter = logging.Formatter("%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s")
#
#     # 1️⃣ Обработчик для stdout (как в задаче 2)
#     stream_handler = logging.StreamHandler(sys.stdout)
#     stream_handler.setFormatter(formatter)
#
#     # 2️⃣ Обработчик для DEBUG и INFO (записывает в calc_debug.log)
#     debug_handler = logging.FileHandler("logs/calc_debug.log", mode="w", encoding="utf-8")
#     debug_handler.setLevel(logging.DEBUG)  # Записываем DEBUG и выше
#     debug_handler.setFormatter(formatter)
#
#     # 3️⃣ Обработчик для ERROR и выше (записывает в calc_error.log)
#     error_handler = logging.FileHandler("logs/calc_error.log", mode="w", encoding="utf-8")
#     error_handler.setLevel(logging.ERROR)  # Только ошибки и выше
#     error_handler.setFormatter(formatter)
#
#     # Добавляем обработчики в root-логгер
#     root_logger.setLevel(logging.DEBUG)
#     root_logger.addHandler(stream_handler)
#     root_logger.addHandler(debug_handler)
#     root_logger.addHandler(error_handler)