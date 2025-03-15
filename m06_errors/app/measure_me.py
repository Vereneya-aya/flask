import logging
import time
import random

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат логов
    handlers=[
        logging.FileHandler("measure.log"),  # Запись в файл
        logging.StreamHandler()  # Вывод в консоль
    ]
)

logger = logging.getLogger(__name__)


def measure_me():
    """Функция, время выполнения которой мы измеряем."""
    logger.info("Enter measure_me")  # Лог перед выполнением
    start_time = time.time()  # Засекаем время начала

    time.sleep(random.uniform(0.1, 0.5))  # Имитация работы (100-500 мс)

    end_time = time.time()  # Засекаем время окончания
    logger.info("Leave measure_me")  # Лог после выполнения

    return end_time - start_time  # Возвращаем время выполнения


# Запуск функции несколько раз для сбора логов
if __name__ == "__main__":
    times = [measure_me() for _ in range(5)]  # Запускаем 5 раз
    avg_time = sum(times) / len(times)  # Среднее время выполнения
    print(f"Среднее время выполнения: {avg_time:.4f} секунд")