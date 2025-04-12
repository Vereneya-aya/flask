import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import math

def factorial_task(n):
    return math.factorial(n)

numbers = [10000, 20000, 30000, 40000]

if __name__ == "__main__":
    # Sequential
    start = time.time()
    results_seq = [factorial_task(n) for n in numbers]
    end = time.time()
    print(f"Sequential execution time: {end - start:.4f} seconds")

    # ThreadPoolExecutor
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        results_thread = list(executor.map(factorial_task, numbers))
    end = time.time()
    print(f"ThreadPoolExecutor time: {end - start:.4f} seconds")

    # ProcessPoolExecutor
    start = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        results_proc = list(executor.map(factorial_task, numbers))
    end = time.time()
    print(f"ProcessPoolExecutor time: {end - start:.4f} seconds")