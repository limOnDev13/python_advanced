import multiprocessing
from multiprocessing import Pool
import math, decimal
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


SUM_FACTORIALS: int = 0


# def worker(queue: multiprocessing.Queue) -> None:
#     """Функция - воркер. Извлекает число из очереди (в очереди просто натуральные числа) и возвращает его факториал"""
#     while not queue.empty():
#         number: int = queue.get()
#         factorial = math.factorial(number)
#
#         logger.info(f'Факториал числа {number} равен {factorial}')
#
#         global SUM_FACTORIALS
#         SUM_FACTORIALS += math.factorial(number)
#         logger.debug(f'SUM_FACTORIAL = {SUM_FACTORIALS}')
#
#
# def sum_all_factorials(max_number: int = 100_000) -> int:
#     global SUM_FACTORIALS
#     SUM_FACTORIALS = 0
#
#     queue = multiprocessing.Queue()
#     for i in range(1, max_number):
#         queue.put(i)
#
#     pool: Pool = Pool(
#         processes=multiprocessing.cpu_count(),
#         initializer=worker,
#         initargs=(queue, )
#     )
#
#     queue.close()
#     queue.join_thread()
#
#     pool.close()
#     pool.join()
#
#     return SUM_FACTORIALS


def task(number: int):
    factorial: int = math.factorial(number)

    logger.debug(f'Факториал числа {number}  равен {format(decimal.Decimal(factorial), '.2e')}')
    return factorial


def sum_all_factorials(number: int = 1_000_00):
    input_values: range = range(1, number)
    with Pool(processes=multiprocessing.cpu_count()) as pool:
        result = pool.map_async(task, input_values)
        result_list: list = result.get()

        return sum(result_list)


if __name__ == "__main__":
    print(f'Сумма факториалов = {format(decimal.Decimal(sum_all_factorials()), '.2e')}')
