import getpass
import hashlib
import logging
import re

# Создаем логер
logger = logging.getLogger("PasswordChecker")
logger.setLevel(logging.DEBUG)  # Отображаем все уровни логов

# Создаем обработчик и форматтер
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def check_password_complexity(password):
    """Проверяет, соответствует ли пароль требованиям сложности."""
    if len(password) < 8:
        logger.warning("Пароль слишком короткий. Минимум 8 символов.")
        return False
    if not re.search(r"\d", password):
        logger.warning("Пароль должен содержать хотя бы одну цифру.")
        return False
    if not re.search(r"[A-Za-z]", password):
        logger.warning("Пароль должен содержать хотя бы одну букву.")
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        logger.warning("Пароль должен содержать хотя бы один спецсимвол.")
        return False
    return True

def input_and_check_password():
    """Запрашивает у пользователя пароль, проверяет его сложность и хэширует."""
    password = getpass.getpass("Введите пароль: ")

    if not password:
        logger.warning("Введен пустой пароль.")
        return False

    if not check_password_complexity(password):
        logger.warning("Пароль не соответствует требованиям.")
        return False

    try:
        hasher = hashlib.md5()
        hasher.update(password.encode('latin-1'))
        hashed_password = hasher.hexdigest()
        logger.info(f"Пароль принят, его хэш: {hashed_password}")
        return True
    except ValueError as e:
        logger.exception("Ошибка при обработке пароля.")
        return False

if __name__ == "__main__":
    count_number = 3
    logger.info(f"У вас есть {count_number} попытки(ок) ввести пароль.")

    while count_number > 0:
        if input_and_check_password():
            logger.info("Пароль успешно принят.")
            break
        count_number -= 1
        logger.warning(f"Осталось попыток: {count_number}")

    if count_number == 0:
        logger.error("Пользователь трижды ввел неправильный пароль.")