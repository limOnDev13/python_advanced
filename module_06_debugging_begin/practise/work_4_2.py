"""
Ниже представлен endpoint, который принимают в POST массив чисел (в виде json),
сортируют его одним из 3х алгоритмов и возвращают пользователю ответ.
Три применяемых алгоритма сортировки - сортировка пузырьком (bubble sort)
timsort (стандартная сортировка python) и сортировка кучей (heap sort).

Расставьте debug логирование в каждой функции логирования так,
чтобы по логам можно было понять сколько времени выполняется каждая функция.

Какая же сортировка в итоге выполняется быстрее?
"""

import heapq
import json
import logging
import time
from typing import List, Callable, Any

from flask import Flask, request

app = Flask(__name__)

logger = logging.getLogger("sort")


def logging_time(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        logger.info(f'Началась сортировка {func.__name__}.')
        start_time: float = time.time()
        result = func(*args, **kwargs)
        logger.info('Время работы сортировки {algorithm}: {time:.5e}'.format(
            algorithm=func.__name__,
            time=time.time() - start_time
        ))
        return result
    return wrapper


@logging_time
def bubble_sort(array: List[int]) -> List[int]:
    n = len(array)

    for i in range(n):
        for j in range(i + 1, n):
            if array[i] > array[j]:
                array[i], array[j] = array[j], array[i]

    return array


@logging_time
def tim_sort(array: List[int]) -> List[int]:
    array.sort()

    return array


@logging_time
def heap_sort(array: List[int]) -> List[int]:
    data = []

    for val in array:
        heapq.heappush(data, val)

    return [heapq.heappop(data) for _ in range(len(data))]


algorithms = {
        "bubble": bubble_sort,
        "tim": tim_sort,
        "heap": heap_sort,
}


@app.route("/<algorithm_name>/", methods=["POST"])
def sort_endpoint(algorithm_name: str):
    if algorithm_name not in algorithms:
        return f"Bad algorithm name, acceptable values are {algorithms.keys()}", 400

    form_data = request.get_data(as_text=True)

    array = json.loads(form_data)

    result = algorithms[algorithm_name](array['array'])

    return json.dumps(result)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Started sort server")
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
