import logging

class AsciiFilter(logging.Filter):
    """Фильтр, который пропускает только ASCII-сообщения"""
    def filter(self, record):
        return record.getMessage().isascii()

# Настроим логгер
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создадим обработчик и добавим фильтр
handler = logging.StreamHandler()
handler.addFilter(AsciiFilter())

# Форматтер и привязка к обработчику
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Добавим обработчик к логгеру
logger.addHandler(handler)

# Тест логов
logger.info("This is ASCII only")  # Пройдет
logger.info("Привет, мир!")  # Не пройдет
logger.info("ASCII & Юникод!")  # Не пройдет