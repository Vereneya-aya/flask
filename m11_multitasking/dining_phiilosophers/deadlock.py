import threading
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

class Philosopher(threading.Thread):
    running = True

    def __init__(self, index, left_fork, right_fork):
        super().__init__()
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork

    def run(self):
        while self.running:
            logging.info(f"Философ {self.index} размышляет 🧠")
            time.sleep(1)
            self.dine()

    def dine(self):
        with self.left_fork:  # Берём левую вилку
            logging.info(f"Философ {self.index} взял левую вилку 🍴")
            time.sleep(0.5)  # Даем шанс другим потокам выполнить действия
            with self.right_fork:  # Берём правую вилку
                logging.info(f"Философ {self.index} взял правую вилку 🍴 и теперь ест 🍝")
                time.sleep(1)
                logging.info(f"Философ {self.index} закончил есть и положил вилки")

if __name__ == "__main__":
    forks = [threading.Lock() for _ in range(5)]
    philosophers = [Philosopher(i, forks[i], forks[(i + 1) % 5]) for i in range(5)]

    for p in philosophers:
        p.start()

    time.sleep(10)
    Philosopher.running = False  # Останавливаем философов

    for p in philosophers:
        p.join()

    logging.info("Все философы закончили обед")