import logging
import random
import threading
import time
import queue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Task:
    def __init__(self, priority, action, args=()):
        self.priority = priority
        self.action = action
        self.args = args

    def __lt__(self, other):
        return self.priority < other.priority

    def run(self):
        logger.info(f"Running Task(priority={self.priority})")
        self.action(*self.args)


class Producer(threading.Thread):
    def __init__(self, task_queue):
        super().__init__()
        self.task_queue = task_queue

    def run(self):
        logger.info("Producer: Running")
        for _ in range(10):
            priority = random.randint(0, 5)
            task = Task(priority, time.sleep, (random.uniform(0.1, 0.5),))
            self.task_queue.put(task)

        # Используем Task-заглушку вместо None
        self.task_queue.put(Task(float('inf'), lambda: None))
        logger.info("Producer: Done")


class Consumer(threading.Thread):
    def __init__(self, task_queue):
        super().__init__()
        self.task_queue = task_queue

    def run(self):
        logger.info("Consumer: Running")
        while True:
            task = self.task_queue.get()
            if task.priority == float('inf'):
                break
            task.run()
            self.task_queue.task_done()

        logger.info("Consumer: Done")


def main():
    task_queue = queue.PriorityQueue()
    producer = Producer(task_queue)
    consumer = Consumer(task_queue)

    producer.start()
    consumer.start()

    producer.join()
    task_queue.join()
    consumer.join()

    logger.info("Processing complete.")


if __name__ == "__main__":
    main()
