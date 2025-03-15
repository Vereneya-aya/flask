import getpass
import hashlib
import logging
import re
import json
import os

# Настроим логгер с JSON-форматом
class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        log_record = {"time": self.format_time(), "level": kwargs.get("level", "INFO"), "message": msg}
        return json.dumps(log_record, ensure_ascii=False), kwargs  # ✅ Теперь правильное формирование JSON-строки

    def format_time(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")

logger = logging.getLogger("PasswordChecker")
logger.setLevel(logging.INFO)

# Логгер в консоль
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Логгер в JSON-файл
json_handler = logging.FileHandler("fixtures/skillbox_json_messages.log", mode="a")
json_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(json_handler)

logger = JsonAdapter(logger)

# Загружаем список английских слов для быстрой проверки
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORDS_FILE = os.path.join(BASE_DIR, "fixtures", "words.txt")

def load_english_words():
    try:
        with open(WORDS_FILE, "r") as f:
            words = {line.strip().lower() for line in f if len(line.strip()) > 4}
        logger.info(f"Загружено {len(words)} английских слов.")
        return words
    except FileNotFoundError:
        logger.error(f"Файл {WORDS_FILE} не найден. Проверьте путь!")
        return set()

english_words = load_english_words()

# Проверка на наличие английских слов в пароле
def is_strong_password(password):
    password = password.lower()
    words_in_password = re.findall(r"[a-zA-Z]+", password)
    for word in words_in_password:
        if word in english_words:
            logger.warning(f"Пароль содержит слово {word} из словаря. Он не подходит.")
            return False
    return True

# Основная проверка сложности пароля
def check_password_complexity(password):
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
    if not is_strong_password(password):
        logger.warning("Пароль содержит английское слово и не является сложным.")
        return False
    return True

# Ввод и проверка пароля пользователем
def input_and_check_password():
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
