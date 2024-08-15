"""Модуль отвечает за работу с бд, которая хранит информацию о пользователях и их картинок. БД - redis"""
from redis import Redis
from typing import Optional
import json
import os
import logging


db_logger = logging.getLogger('utils_logger')


def _del_all_files_in_dir(dir_path: str = './static/blured_images') -> None:
    """Функция удаляет все файлы из директории"""
    db_logger.info(f'Starting removing files in {dir_path}')
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        db_logger.debug(f'file_path = {file_path}')

        try:
            os.remove(file_path)
            db_logger.debug('Removed')
        except Exception as exc:
            db_logger.exception(f'Error deleting a file {file_path}', exc_info=exc)


class UserImages:
    """
    Класс - хранилище данных о пользователях и их групп изображений

    Args:
        host (str) - Хост redis
        port (int) - Порт redis
    """
    def __init__(self, host: str = 'localhost', port: int = 6379):
        self.__r: Redis = Redis(
            host=host,
            port=port,
            charset='utf-8',
            decode_responses=True
        )
        self.__dict_name: str = 'users'

    def get(self) -> Optional[dict[str, list[str]]]:
        """Метод возвращает словарь с email-ми получателей и их списков групп изображений"""
        return json.loads(self.__r.get(self.__dict_name))

    def add(self, receiver: str, groups: Optional[list[str]] = None) -> bool:
        """Метод добавляет пользователя в бд. Если передан список group_id обработанных изображений,
        также сохраняет информацию. Если пользователь уже есть в бд - добавляет изображения
         если они есть и возвращает True. Если пользователя нет - добавит изображения и вернет False"""
        db_logger.info(f'Adding receiver {receiver} with groups {groups}')
        redis_dict_str: str = self.__r.get(self.__dict_name)
        db_logger.debug(f'1) redis_dict_str: {redis_dict_str}')

        if redis_dict_str:
            redis_dict: dict[str, list[str]] = json.loads(redis_dict_str)
        else:
            redis_dict: dict[str, list[str]] = dict()

        db_logger.debug(f'2) redis_dict = {redis_dict}')

        user_was_in_db: bool = False

        if receiver not in redis_dict:
            user_was_in_db = True
            redis_dict[receiver] = list()

        db_logger.debug(f'3) redis_dict[receiver] before adding group: {redis_dict[receiver]}')
        if groups:
            redis_dict[receiver].extend(groups)
        db_logger.debug(f'4) redis_dict[receiver] after adding group: {redis_dict[receiver]}')

        self.__r.set(self.__dict_name, json.dumps(redis_dict))
        db_logger.debug(f'5) After all redis_dict_str = {self.__r.get(self.__dict_name)}')

        return user_was_in_db

    def remove(self, receiver: str) -> list[str]:
        """Метод удаляет получателя из бд. Возвращает хранимые группы изображений у этого пользователя"""
        redis_dict_str: str = self.__r.get(self.__dict_name)

        if not redis_dict_str:
            raise ValueError('Db is empty')

        redis_dict: dict[str, list[str]] = json.loads(redis_dict_str)

        if receiver not in redis_dict:
            raise ValueError('User is not found')
        groups: list[str] = redis_dict.pop(receiver)

        self.__r.set(self.__dict_name, json.dumps(redis_dict))
        return groups

    def clear(self) -> None:
        """Метод удаляет данные о всех изображениях (email-ы пользователей остаются).
        Метод будет вызываться после рассылки, чтобы не хранить информацию об изображениях.
        Изображения также будут удаляться"""
        # 1) Удалим изображения
        _del_all_files_in_dir('./static/blured_images')
        # 2) Почистим бд
        redis_dict_str: str = self.__r.get(self.__dict_name)
        redis_dict: dict[str, list[str]] = json.loads(redis_dict_str)

        if len(redis_dict) == 0:
            db_logger.warning('Db is empty')
        else:
            for user in redis_dict.keys():
                redis_dict[user].clear()

            self.__r.set(self.__dict_name, json.dumps(redis_dict))


if __name__ == '__main__':
    db = UserImages()
    db.add('1')
    db.clear()
