import logging
import logging.config

class AsciiFilter(logging.Filter):
    def filter(self, record):
        return record.getMessage().isascii()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "ascii_filter": {
            "()": AsciiFilter  # Создание экземпляра фильтра
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "filters": ["ascii_filter"]
        }
    },
    "formatters": {
        "default": {
            "format": "%(levelname)s - %(message)s"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG"
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Тест
logger.info("Hello, ASCII!")  # Пройдет
logger.info("Привет, мир!")  # Не пройдет