LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "simpleFormatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },

    "handlers": {
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "simpleFormatter",
            "stream": "ext://sys.stdout"
        },
        "fileHandler": {
            "class": "logging.FileHandler",
            "level": "ERROR",
            "formatter": "simpleFormatter",
            "filename": "app.log",
            "mode": "w"
        }
    },

    "loggers": {
        "exampleLogger": {
            "level": "INFO",
            "handlers": ["fileHandler"],
            "propagate": False
        }
    },

    "root": {
        "level": "DEBUG",
        "handlers": ["consoleHandler"]
    }
}