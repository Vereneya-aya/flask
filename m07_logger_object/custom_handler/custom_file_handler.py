import logging
import logging.config
import sys

class CustomStreamHandler(logging.StreamHandler):
    def __init__(self, stream=None):
        if stream is None:
            stream = sys.stderr
        super().__init__(stream)

# Конфигурация логирования
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(name)s || %(levelname)s || %(message)s || %(module)s.%(funcName)s:%(lineno)d || %(very)s"
        }
    },
    "handlers": {
        "custom_stream": {
            "()": CustomStreamHandler,  # Используем кастомный обработчик
            "level": "DEBUG",
            "formatter": "detailed",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "custom_log.log",
            "mode": "a",
            "encoding": "utf-8"
        }
    },
    "loggers": {
        "sub_1": {
            "level": "INFO",
            "handlers": ["custom_stream", "file"],
            "propagate": False
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["custom_stream"]
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
