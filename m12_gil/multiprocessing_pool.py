import time
import multiprocessing


def task(n):
    return sum(i ** 2 for i in range(n))


if __name__ == "__main__":
    numbers = [10 ** 6, 10 ** 6 + 1, 10 ** 6 + 2, 10 ** 6 + 3]

    start_time = time.time()
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(task, numbers)
    end_time = time.time()

    print(f"Results: {results}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")