import threading

counter = 0
lock = threading.Lock()

def worker_1():
    global counter
    for _ in range(1000):
        with lock:  # Блокируем доступ
            counter += 1

def worker_2():
    global counter
    for _ in range(1000):
        with lock:  # Блокируем доступ
            counter -= 1

def main():
    t1 = threading.Thread(target=worker_1)
    t2 = threading.Thread(target=worker_2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"Final counter value: {counter}")

if __name__ == "__main__":
    main()