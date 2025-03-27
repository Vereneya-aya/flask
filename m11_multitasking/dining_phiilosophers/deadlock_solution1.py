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

    def dine(self):
        if self.index % 2 == 0:  # Чётные философы берут правую вилку первой
            first_fork, second_fork = self.right_fork, self.left_fork
        else:
            first_fork, second_fork = self.left_fork, self.right_fork

        with first_fork:
            logging.info(f"Философ {self.index} взял вилку 🍴")
            time.sleep(0.5)
            with second_fork:
                logging.info(f"Философ {self.index} теперь ест 🍝")
                time.sleep(1)
                logging.info(f"Философ {self.index} закончил есть и положил вилки")