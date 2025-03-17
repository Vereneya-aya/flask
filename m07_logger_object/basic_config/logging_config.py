import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(name)s || %(levelname)s || %(message)s || %(module)s.%(funcName)s:%(lineno)d"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "app.log",
            "mode": "a",
            "encoding": "utf-8"
        }
    },
    "loggers": {
        "sub_1": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False
        },
        "sub_2": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False
        },
        "sub_2.sub_sub_1": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"]
    }
}

# logging.config.dictConfig(LOGGING_CONFIG)
