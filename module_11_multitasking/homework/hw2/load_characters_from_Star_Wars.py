import requests
import threading
import time
from typing import Callable, Any
import functools
import logging.config
import sqlite3

from logging_config import dict_config


logging.config.dictConfig(dict_config)
logger = logging.getLogger('module_logger')

URL: str = 'https://swapi.dev/api/people/{}/'


def create_table(db_file: str = 'star_wars_characters.db', table_name: str = 'characters') -> None:
    """Функция создает таблицу для добавления в нее информации о персонажах звездных войн.
    Если таблица уже существует, то она полностью очищается, чтобы не засорять ее при тестировании"""
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        # Если есть таблица - удалим ее
        drop_table_query: str = f"""DROP TABLE IF EXISTS {table_name}"""
        cursor.execute(drop_table_query)

        # создадим новую таблицу
        create_table_query: str = f"""CREATE TABLE {table_name}
        (
            name TEXT,
            url TEXT
        )
        """
        cursor.execute(create_table_query)


def add_character_info_in_db(character_info: dict, db_file: str = 'star_wars_characters.db') -> None:
    """Функция добавляет запись о персонаже из star wars в бд"""
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        insert_query: str = f"""
        INSERT INTO characters (name, url) VALUES ('{character_info['name']}', '{character_info['url']}')
        """
        cursor.execute(insert_query)


def get_character_info(url: str) -> dict:
    """Функция делает запрос к url и возвращает словарь с информацией о персонаже"""
    response = requests.get(url)
    if response.status_code != 200:
        raise requests.HTTPError(response.json())

    logger.debug(f'json = {response.json()}')
    return response.json()


def get_and_save_info(url: str, db_file: str = 'star_wars_characters.db') -> None:
    """Функция делает запрос к url, получает информацию и сохраняет ее в бд (объединение функций
    get_character_info и add_character_info_in_db - нужно, чтобы поместить их в один поток)"""
    try:
        add_character_info_in_db(get_character_info(url), db_file)
    except requests.HTTPError as exc:
        logger.exception('HTTPError', exc_info=exc)


def timer(func: Callable) -> Callable:
    """Функция замеряет время работы оборачиваемой функции"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time: float = time.time()
        result = func(*args, **kwargs)
        logger.info(f'Время работы {func.__name__}: {time.time() - start_time}')
        return result
    return wrapper


@timer
def download_characters_sequentially(number_people: int = 20, db_file: str = 'star_wars_characters.db') -> None:
    """Функция последовательно делает запросы к url и сохраняет информацию в бд"""
    for num in range(1, number_people + 1):
        get_and_save_info(URL.format(num), db_file)


@timer
def download_characters_with_threads(number_people: int = 20, db_file: str = 'star_wars_characters.db') -> None:
    """Функция многопоточно делает запросы к url и сохраняет информацию в бд"""
    threads: list[threading.Thread] = [
        threading.Thread(target=get_and_save_info, args=(URL.format(num), db_file))
        for num in range(number_people)
    ]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    logger.info('Тестируем функцию download_characters_sequentially')
    create_table()
    download_characters_sequentially()
    logger.info('Тестируем функцию download_characters_with_threads')
    create_table()
    download_characters_with_threads()
