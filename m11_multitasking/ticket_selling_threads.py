import logging
import random
import threading
import time

TOTAL_SEATS = 50  # Общее количество мест в кинотеатре
TICKET_THRESHOLD = 5  # Порог, при котором директор пополняет билеты
ADD_TICKETS = 10  # Сколько билетов добавляет директор

tickets_available = 30  # Начальное количество билетов
lock = threading.Lock()

director_event = threading.Event()  # Событие для синхронизации директора

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Seller(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.tickets_sold = 0

    def run(self):
        global tickets_available
        while True:
            time.sleep(random.uniform(0.1, 0.5))
            with lock:
                if tickets_available <= 0:
                    break
                self.tickets_sold += 1
                tickets_available -= 1
                logger.info(f"{self.name} продал билет. Осталось: {tickets_available}")

                if tickets_available <= TICKET_THRESHOLD:
                    director_event.set()

        logger.info(f"{self.name} закончил работу. Продано билетов: {self.tickets_sold}")


class Director(threading.Thread):
    def run(self):
        global tickets_available
        while True:
            director_event.wait()  # Ждём, когда билетов останется мало
            with lock:
                if tickets_available <= 0:
                    break
                new_tickets = min(ADD_TICKETS, TOTAL_SEATS - tickets_available)
                tickets_available += new_tickets
                logger.info(f"Директор добавил {new_tickets} билетов. Всего теперь: {tickets_available}")
                director_event.clear()  # Сбрасываем событие

        logger.info("Директор закончил работу.")


def main():
    sellers = [Seller(f"Касса-{i + 1}") for i in range(3)]
    director = Director()

    director.start()
    for seller in sellers:
        seller.start()

    for seller in sellers:
        seller.join()

    director_event.set()  # Разбудить директора, чтобы он завершился
    director.join()

    logger.info("Продажа билетов завершена.")


if __name__ == "__main__":
    main()
