import time
import multiprocessing
import os


class MySuperClass:
    def __init__(self, name):
        self.name = name

    def do_something(self):
        proc_name = multiprocessing.current_process().name
        proc_pid = os.getpid()
        print(f'Doing something fancy in {proc_name}, pid {proc_pid} for {self.name}!')


def worker(queue):
    while not queue.empty():
        obj = queue.get()
        obj.do_something()
        time.sleep(0.1)


if __name__ == '__main__':
    queue = multiprocessing.Queue()

    for i in range(1, 40):
        queue.put(MySuperClass(f'Object num {i}'))

    pool = multiprocessing.Pool(processes=4, initializer=worker, initargs=(queue,))

    queue.close()
    queue.join_thread()

    pool.close()
    pool.join()