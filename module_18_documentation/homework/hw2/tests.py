"""Модуль для тестирования api (для ответов к задаче)"""
from clients import BookClient
from multiprocessing.pool import ThreadPool
import functools
import time
from typing import Callable, Any
import logging.config
import os
import requests

from logging_config import dict_config


logging.config.dictConfig(dict_config)
logger = logging.getLogger('tests')

URL: str = 'http://127.0.0.1:5000/api/books'


def timer(func: Callable) -> Callable:
    """Функция - декоратор. Измеряет время работы функции"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start: float = time.time()
        result = func(*args, **kwargs)
        logger.debug(f"Function {func.__name__}. Working time: {time.time() - start}")
        return result
    return wrapper


@timer
def execute_with_multithreading(func: Callable, num_queries: int, *args, **kwargs):
    """Функция выполняет функцию многопоточно num_queries раз"""
    logging.debug(f'Количество запросов: {num_queries}')
    with ThreadPool(processes=os.cpu_count()) as pool:
        for _ in range(num_queries):
            pool.apply_async(func, *args, **kwargs)


@timer
def execute_without_multithreading(func: Callable, num_queries: int, *args, **kwargs):
    logger.debug(f'Количество запросов: {num_queries}')
    for _ in range(num_queries):
        func(*args, **kwargs)


NUMS_QUERIES: list = [10, 100, 1000]


class TestWithoutAdditionalSetting:
    SETTING: str = 'БЕЗ настройки,'

    def test(self):
        """Функция отвечает на вопросы задачи (без дополнительной настройки)"""
        client: BookClient = BookClient()

        # С сессией и многопоточностью
        logger.info(self.SETTING + ' с сессией и многопоточностью')
        for num in NUMS_QUERIES:
            execute_with_multithreading(client.get_all_books, num)
        time.sleep(1)

        # С сессией и без многопоточности
        logger.info(self.SETTING + ' с сессией и БЕЗ многопоточности')
        for num in NUMS_QUERIES:
            execute_without_multithreading(client.get_all_books, num)

        # Без сессии и с многопоточностью
        logger.info(self.SETTING + ' БЕЗ сессии и с многопоточностью')
        for num in NUMS_QUERIES:
            execute_with_multithreading(requests.get, num, URL)
        time.sleep(1)

        # Без сессии и без многопоточности
        logger.info(self.SETTING + ' БЕЗ сессии и БЕЗ многопоточности')
        for num in NUMS_QUERIES:
            execute_without_multithreading(requests.get, num, URL)


class TestWithAdditionalSetting(TestWithoutAdditionalSetting):
    SETTING: str = 'C настройкой,'

    def __init__(self):
        from werkzeug.serving import WSGIRequestHandler

        WSGIRequestHandler.protocol_version = "HTTP/1.1"


if __name__ == '__main__':
    test_without_add_setting = TestWithoutAdditionalSetting()
    test_without_add_setting.test()
    test_with_add_setting = TestWithAdditionalSetting()
    test_with_add_setting.test()
