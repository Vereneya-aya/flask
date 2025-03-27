import threading
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

semaphore = threading.Semaphore(4)  # Разрешаем 4 философам есть одновременно

class Philosopher(threading.Thread):
    running = True

    def dine(self):
        while self.running:
            with semaphore:  # Блокируем доступ, если уже 4 философа едят
                with self.left_fork, self.right_fork:
                    logging.info(f"Философ {self.index} ест 🍝")
                    time.sleep(1)