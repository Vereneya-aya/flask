import os
import time
import threading
import multiprocessing
import requests


def get_image(url, result_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(result_path, "wb") as file:
            file.write(response.content)


def load_images_sequential(url, out_dir, count=10):
    start = time.time()
    for i in range(count):
        get_image(url, os.path.join(out_dir, f"{i}.jpg"))
    print(f"Sequential: {time.time() - start:.2f} sec")


def load_images_multithreading(url, out_dir, count=10):
    start = time.time()
    threads = []
    for i in range(count):
        thread = threading.Thread(target=get_image, args=(url, os.path.join(out_dir, f"{i}.jpg")))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print(f"Multithreading: {time.time() - start:.2f} sec")


def load_images_multiprocessing(url, out_dir, count=10):
    start = time.time()
    processes = []
    for i in range(count):
        process = multiprocessing.Process(target=get_image, args=(url, os.path.join(out_dir, f"{i}.jpg")))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    print(f"Multiprocessing: {time.time() - start:.2f} sec")


def task(number):
    return sum(i ** i for i in range(number))


def run_task_sequential(n, count=5):
    start = time.time()
    results = [task(n) for _ in range(count)]
    print(f"Sequential: {time.time() - start:.2f} sec")
    return results


def run_task_multithreading(n, count=5):
    start = time.time()
    threads = []
    for _ in range(count):
        thread = threading.Thread(target=task, args=(n,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print(f"Multithreading: {time.time() - start:.2f} sec")


def run_task_multiprocessing(n, count=5):
    start = time.time()
    processes = []
    for _ in range(count):
        process = multiprocessing.Process(target=task, args=(n,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    print(f"Multiprocessing: {time.time() - start:.2f} sec")


if __name__ == "__main__":
    os.makedirs("temp", exist_ok=True)
    image_url = "https://cataas.com/cat"

    print("\nTesting Image Downloading...")
    load_images_sequential(image_url, "temp", count=10)
    load_images_multithreading(image_url, "temp", count=10)
    load_images_multiprocessing(image_url, "temp", count=10)

    print("\nTesting Computational Task...")
    run_task_sequential(10 ** 3, count=5)
    run_task_multithreading(10 ** 3, count=5)
    run_task_multiprocessing(10 ** 3, count=5)
