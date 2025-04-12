from threading import Semaphore, Thread
import time
import signal
import sys

sem = Semaphore()
running = True  # Флаг для управления потоками

def fun1():
    while running:
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)

def fun2():
    while running:
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)

def signal_handler(sig, frame):
    global running
    print('\nПолучен сигнал завершения. Остановка потоков...')
    running = False  # Меняем флаг, чтобы остановить циклы
    time.sleep(0.5)  # Даём время потокам завершиться
    sys.exit(0)

# Перехватываем сигнал Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Запускаем потоки
t1 = Thread(target=fun1)
t2 = Thread(target=fun2)
t1.start()
t2.start()

t1.join()
t2.join()
