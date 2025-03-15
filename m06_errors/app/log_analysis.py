import json
import re
from collections import Counter
from itertools import groupby

LOG_FILE = "fixtures/skillbox_json_messages.log"

def load_logs():
    """Загружает логи из файла и возвращает список JSON-объектов"""
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) for line in f]

logs = load_logs()

# 1️⃣ Подсчет количества логов каждого уровня
log_levels = Counter(log["level"] for log in logs)

# 2️⃣ Час с наибольшим количеством логов
logs_by_hour = Counter(log["time"][:2] for log in logs)  # time[:2] — берём часы
most_active_hour = max(logs_by_hour, key=logs_by_hour.get)

# 3️⃣ Количество CRITICAL логов с 05:00:00 по 05:20:00
critical_logs = sum(1 for log in logs if log["level"] == "CRITICAL" and "05:00:00" <= log["time"] <= "05:20:00")

# 4️⃣ Сколько сообщений содержат слово "dog"
dog_logs = sum(1 for log in logs if "dog" in log["message"].lower())

# 5️⃣ Самое частое слово в WARNING логах
warning_messages = " ".join(log["message"] for log in logs if log["level"] == "WARNING")
words = re.findall(r"\b\w+\b", warning_messages.lower())  # Разбиваем текст на слова

most_common_word = Counter(words).most_common(1)  # Получаем [(слово, кол-во)]
most_common_word = most_common_word[0][0] if most_common_word else "Нет данных"



# 🔥 Вывод результатов
print(f"📊 Количество логов каждого уровня: {dict(log_levels)}")
print(f"⏳ Час с наибольшим числом логов: {most_active_hour}:00")
print(f"🚨 Количество CRITICAL логов с 05:00:00 до 05:20:00: {critical_logs}")
print(f"🐶 Количество сообщений с 'dog': {dog_logs}")
print(f"⚠️ Самое частое слово в WARNING логах: {most_common_word}")