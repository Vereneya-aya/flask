import configparser
import json
import sys

def ini_to_dict(ini_path):
    config = configparser.ConfigParser(interpolation=None)  # <--- Отключаем интерполяцию
    config.read(ini_path)

    log_dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {},
        "handlers": {},
        "loggers": {},
        "root": {}
    }

    # Форматтеры
    for key in config.get("formatters", "keys").split(","):
        log_dict["formatters"][key] = {
            "format": config.get(f"formatter_{key}", "format"),
            "datefmt": config.get(f"formatter_{key}", "datefmt", fallback=None)
        }

    # Обработчики
    for key in config.get("handlers", "keys").split(","):
        log_dict["handlers"][key] = {
            "class": config.get(f"handler_{key}", "class"),
            "level": config.get(f"handler_{key}", "level"),
            "formatter": config.get(f"handler_{key}", "formatter"),
        }
        if config.has_option(f"handler_{key}", "args"):
            args = eval(config.get(f"handler_{key}", "args"))
            if isinstance(args, tuple):
                args = list(args)
            if "FileHandler" in log_dict["handlers"][key]["class"]:
                log_dict["handlers"][key]["filename"] = args[0]
                log_dict["handlers"][key]["mode"] = args[1]

    # Логгеры
    for key in config.get("loggers", "keys").split(","):
        log_dict["loggers"][key] = {
            "level": config.get(f"logger_{key}", "level"),
            "handlers": config.get(f"logger_{key}", "handlers").split(","),
            "propagate": config.getboolean(f"logger_{key}", "propagate", fallback=True)
        }

    # Root логгер
    log_dict["root"] = {
        "level": config.get("logger_root", "level"),
        "handlers": config.get("logger_root", "handlers").split(",")
    }

    return log_dict

# Пример использования
config_dict = ini_to_dict("logging_conf.ini")

# Сохраняем в JSON для удобства
with open("logging_conf.json", "w") as f:
    json.dump(config_dict, f, indent=4)

print(json.dumps(config_dict, indent=4))