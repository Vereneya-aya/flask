import threading
import time
import random

TOTAL_TICKETS = 10
tickets = TOTAL_TICKETS
semaphore = threading.BoundedSemaphore(1)  # Разрешаем 1 потоку одновременно

class Seller(threading.Thread):
    def run(self):
        global tickets
        while True:
            time.sleep(random.uniform(0.1, 0.5))  # Симуляция работы кассы

            with semaphore:  # Только 1 поток за раз
                if tickets > 0:
                    tickets -= 1
                    print(f"{self.name} продал билет. Осталось: {tickets}")
                else:
                    print(f"{self.name} увидел, что билетов больше нет.")
                    break  # Останавливаем поток

        # Попробуем вызвать release() больше раз, чем разрешено
        semaphore.release()  # Это вызовет исключение при превышении лимита

def main():
    sellers = [Seller() for _ in range(3)]  # Создаём 3 кассира

    for seller in sellers:
        seller.start()

    for seller in sellers:
        seller.join()

    print("Продажа завершена.")

if __name__ == "__main__":
    main()