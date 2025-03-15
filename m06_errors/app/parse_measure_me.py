import re
from datetime import datetime

def parse_log(file_path):
    """Функция для вычисления среднего времени выполнения measure_me"""
    with open(file_path, "r") as file:
        logs = file.readlines()

    timestamps = []
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+) - INFO - (Enter|Leave) measure_me"

    for line in logs:
        match = re.search(pattern, line)
        if match:
            timestamps.append((match.group(2), datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S,%f")))

    times = []
    for i in range(0, len(timestamps), 2):
        start, end = timestamps[i][1], timestamps[i+1][1]
        times.append((end - start).total_seconds())

    avg_time = sum(times) / len(times) if times else 0
    print(f"Среднее время выполнения: {avg_time:.4f} секунд")

# Анализируем файл логов
parse_log("measure.log")