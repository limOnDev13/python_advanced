import time
import logging
from multiprocessing import Pool, cpu_count

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def task(number):
    try:
        return sum(i ** i for i in range(number))
    except Exception as exc:
        logger.exception('Произошла ошибка в task', exc_info=exc)


def high_load_map():
    start = time.time()
    input_value = [f'{i}' for i in range(1, 1000, 100)]

    with Pool(processes=cpu_count()) as pool:
        result = pool.map(task, input_value)

    end = time.time()
    logger.info(f'Time taken in seconds - {end - start}')
    logger.info(len(result))


if __name__ == '__main__':
    high_load_map()
