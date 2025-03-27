import logging
import threading
import random
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Philosopher(threading.Thread):
    running = True

    def __init__(self, left_fork: threading.Lock, right_fork: threading.Lock):
        super().__init__()
        self.left_fork = left_fork
        self.right_fork = right_fork

    def run(self):
        while self.running:
            logger.info(f'Philosopher {self.getName()} is thinking.')
            time.sleep(random.uniform(1, 3))  # Более реалистичное время ожидания
            logger.info(f'Philosopher {self.getName()} is hungry.')

            # Используем контекстный менеджер для блокировок
            with self.left_fork:
                logger.info(f'Philosopher {self.getName()} acquired left fork.')

                with self.right_fork:
                    logger.info(f'Philosopher {self.getName()} acquired right fork.')
                    self.dining()

    def dining(self):
        logger.info(f'Philosopher {self.getName()} starts eating.')
        time.sleep(random.uniform(1, 3))
        logger.info(f'Philosopher {self.getName()} finishes eating and leaves to think.')


def main():
    forks = [threading.Lock() for _ in range(5)]
    philosophers = [
        Philosopher(forks[i % 5], forks[(i + 1) % 5])
        for i in range(5)
    ]

    Philosopher.running = True
    for p in philosophers:
        p.start()

    time.sleep(20)  # Даем философам поработать
    Philosopher.running = False

    for p in philosophers:
        p.join()

    logger.info("Now we're finishing.")


if __name__ == "__main__":
    main()
