import logging

logger = logging.getLogger("utils")  # Теперь явно используем логгер utils

def add(x, y):
    result = x + y
    logger.info(f"Сложение {x} + {y} = {result}")
    return result

def subtract(x, y):
    result = x - y
    logger.info(f"Вычитание {x} - {y} = {result}")
    return result

def multiply(x, y):
    result = x * y
    logger.info(f"Умножение {x} * {y} = {result}")
    return result

def divide(x, y):
    if y == 0:
        logger.error("Попытка деления на ноль")
        return None
    result = x / y
    logger.info(f"Деление {x} / {y} = {result}")
    return result