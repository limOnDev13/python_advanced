import threading
import time
import logging
from queue import PriorityQueue
import requests
import dataclasses


logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    datefmt='%D.%M.%Y',
    filename='output_logs.log',
    filemode='w'
)
logger = logging.getLogger(__name__)
QUEUE: PriorityQueue = PriorityQueue()


@dataclasses.dataclass(order=True)
class DateAndTimestamp:
    priority: float
    date: str


def get_timestamp_from_url(barrier: threading.Barrier,
                           base_url: str = 'http://127.0.0.1:8080/timestamp/',
                           timeout: int = 20) -> None:
    """
    Функция получает с url дату по текущему timestamp по не закончится timeout. Полученная дата сохраняется в
    приоритетную очередь с приоритетом timestamp. Функция выполняется раз в 1 сек
    :param barrier: Нужен для синхронизации потоков
    :param base_url: Базовый url. С помощью него передается текущий timestamp
    :param timeout: Таймаут работы функции
    :return: None
    """
    start: float = time.time()
    while time.time() - start < timeout:
        timestamp: float = time.time()
        response = requests.get(base_url + f'{time.time()}')
        date_from_url: str = response.text.split()[0]
        QUEUE.put(DateAndTimestamp(timestamp, date_from_url))
        time.sleep(1)

    barrier.wait()


def save_logs_in_file() -> None:
    while not QUEUE.empty():
        log_data: DateAndTimestamp = QUEUE.get()
        logger.info(f'<{log_data.priority}> <{log_data.date}>')


def create_threads(number_threads: int = 10,
                   base_url: str = 'http://127.0.0.1:8080/timestamp/',
                   timeout: int = 20) -> None:
    """Функция создает number_threads потоков, которые получают дату с url по timestamp и
     добавляют информацию в приоритетную очередь. Когда потоки отработают - функция запишет информацию в лог файл.
     Потоки запускаются раз в секунду"""
    barrier: threading.Barrier = threading.Barrier(number_threads + 1)
    threads: list[threading.Thread] = [threading.Thread(target=get_timestamp_from_url,
                                                        args=(barrier, base_url, timeout,))
                                       for _ in range(number_threads)]
    for thread in threads:
        thread.start()
        time.sleep(1)

    barrier.wait()
    save_logs_in_file()


if __name__ == "__main__":
    create_threads()
