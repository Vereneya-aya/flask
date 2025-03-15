import heapq
import json
import logging
import time
from typing import List

from flask import Flask, request, jsonify

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("sort")

def bubble_sort(array: List[int]) -> List[int]:
    logger.debug(f"Начинаем bubble_sort: {array}")
    start_time = time.perf_counter()

    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]

    end_time = time.perf_counter()
    logger.debug(f"Bubble sort завершён за {end_time - start_time:.6f} сек")
    return array

def tim_sort(array: List[int]) -> List[int]:
    logger.debug(f"Начинаем tim_sort: {array}")
    start_time = time.perf_counter()

    array.sort()

    end_time = time.perf_counter()
    logger.debug(f"Timsort завершён за {end_time - start_time:.6f} сек")
    return array

def heap_sort(array: List[int]) -> List[int]:
    logger.debug(f"Начинаем heap_sort: {array}")
    start_time = time.perf_counter()

    heapq.heapify(array)
    sorted_array = [heapq.heappop(array) for _ in range(len(array))]

    end_time = time.perf_counter()
    logger.debug(f"Heap sort завершён за {end_time - start_time:.6f} сек")
    return sorted_array

# Словарь с алгоритмами
algorithms = {
    "bubble": bubble_sort,
    "tim": tim_sort,
    "heap": heap_sort,
}

@app.route("/<algorithm_name>/", methods=["POST"])
def sort_endpoint(algorithm_name: str):
    if algorithm_name not in algorithms:
        return jsonify({"error": f"Неверное имя алгоритма, доступные: {list(algorithms.keys())}"}), 400

    try:
        data = request.get_json()
        if not data or "numbers" not in data:
            return jsonify({"error": "JSON должен содержать ключ 'numbers' с массивом"}), 400

        array = data["numbers"]
        if not isinstance(array, list) or not all(isinstance(i, int) for i in array):
            return jsonify({"error": "Массив должен содержать только числа"}), 400

        logger.info(f"Принят запрос для {algorithm_name}, входные данные: {array}")

        sorted_array = algorithms[algorithm_name](array.copy())  # Копируем, чтобы не менять входные данные

        logger.info(f"Результат сортировки: {sorted_array}")
        return jsonify({"sorted_numbers": sorted_array})

    except Exception as e:
        logger.error(f"Ошибка обработки запроса: {str(e)}")
        return jsonify({"error": "Ошибка обработки запроса"}), 500

if __name__ == "__main__":
    logger.info("Запуск сервера Flask для сортировки")
    app.run(debug=True)

# import requests
#
# url = "http://127.0.0.1:5000/tim/"
# data = {"numbers": [10, 3, 8, 2]}
# response = requests.post(url, json=data)
# print(response.json())