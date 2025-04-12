import threading
import time
import requests
from queue import PriorityQueue

LOG_FILE = "logs.txt"
NUM_THREADS = 10
LOG_DURATION = 20  # секунд

queue = PriorityQueue()


def log_worker(thread_id):
    """Функция для потоков, записывает логи с временной меткой."""
    end_time = time.time() + LOG_DURATION
    while time.time() < end_time:
        timestamp = int(time.time())
        try:
            response = requests.get(f"http://127.0.0.1:8080/timestamp/{timestamp}", timeout=3)
            response.raise_for_status()  # Выбросит ошибку, если статус не 200
            log_entry = f"{timestamp} {response.text.strip()}"
            queue.put((timestamp, log_entry))
        except requests.RequestException as e:
            print(f"[Ошибка потока {thread_id}] {e}")
        time.sleep(1)


def write_logs():
    """Функция для записи логов из очереди в файл в порядке сортировки по timestamp."""
    with open(LOG_FILE, "w") as f:
        while not queue.empty():
            _, log_entry = queue.get()
            f.write(log_entry + "\n")


if __name__ == "__main__":
    threads = []

    for i in range(NUM_THREADS):
        thread = threading.Thread(target=log_worker, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    write_logs()
    print("Логи записаны в файл", LOG_FILE)