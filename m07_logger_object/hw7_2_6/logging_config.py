LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "detailed": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "stream": "ext://sys.stdout"
        },
        "debug_file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "logs/calc_debug.log",
            "mode": "w",
            "encoding": "utf-8"
        },
        "error_file": {
            "class": "logging.FileHandler",
            "level": "ERROR",
            "formatter": "detailed",
            "filename": "logs/calc_error.log",
            "mode": "w",
            "encoding": "utf-8"
        },
        "utils_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "detailed",
            "filename": "logs/utils.log",
            "when": "H",  # Ротация раз в час
            "interval": 10,  # Каждые 10 часов
            "backupCount": 1,  # Храним только одну старую копию
            "encoding": "utf-8"
        }
    },

    "loggers": {
        "utils": {
            "level": "INFO",
            "handlers": ["utils_file"],
            "propagate": False
        }
    },

    "root": {
        "level": "DEBUG",
        "handlers": ["console", "debug_file", "error_file"]
    }
}