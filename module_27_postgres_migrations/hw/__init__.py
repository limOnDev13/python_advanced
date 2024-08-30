from flask import Flask
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.orm import sessionmaker
import requests
from typing import List
import time
import random
import logging.config

from .models import Base, User, Coffee
from .log_config import dict_config


logging.config.dictConfig(dict_config)
logger = logging.getLogger('init_logger')

app = Flask(__name__)
engine = create_engine('postgresql://admin:admin@localhost')
Session = sessionmaker(bind=engine)
session = Session()

RANDOM_USER_URL: str = 'https://random-data-api.com/api/v3/projects/29421519-d2ee-48e9-ad13-c2bca4bb3eae?api_key=z82-T2rJM5-PapGypxi_ZA'
RANDOM_ADDRESS_URL: str = 'https://random-data-api.com/api/address/random_address'
RANDOM_COFFEE_URL: str = 'https://random-data-api.com/api/coffee/random_coffee'


def random_coffee(num_coffee: int = 10) -> List[Coffee]:
    """Функция возвращает словарь с генерированным кофе"""
    coffee_list: List[dict] = list()
    counter: int = 0
    while len(coffee_list) < num_coffee:
        try:
            logger.debug(f'{counter} попытка получения рандомного кофе')
            response = requests.get(RANDOM_COFFEE_URL)
            coffee = response.json()
            logger.debug(f'Получено coffee = {coffee}')
            coffee_list.append(coffee)
            time.sleep(2)  # Задержка, чтобы избежать 429 кода ответа
            counter += 1
        except Exception as exc:
            logger.exception('Попытка провалилась', exc_info=exc)
        else:
            logger.debug(f'Попытка успешная')

    return [Coffee(title=coffee['blend_name'],
                   origin=coffee['origin'],
                   intensifier=coffee['intensifier'],
                   notes=coffee['notes'])
            for coffee in coffee_list
            ]


def random_user(coffe_ids: list[int], num_users: int = 10) -> List[User]:
    """Функция возвращает словарь с генерированными пользователями"""
    users: List[User] = list()
    idx: int = 1

    while len(users) < num_users:
        try:
            logger.debug(f'{idx - 1} попытка получения рандомного пользователя')
            address = requests.get(RANDOM_ADDRESS_URL).json()
            logger.debug(f'Получен address = {address}')
            time.sleep(2)
            user = requests.get(RANDOM_USER_URL).json()
            logger.debug(f'Получен user = {user}')
            user['address'] = address
            users.append(user)
            idx += 1
            time.sleep(2)
        except Exception as exc:
            logger.exception('Попытка провалилась', exc_info=exc)
        else:
            logger.debug('Попытка успешная')

    return [User(name=user['name'],
                 # has_sale=user['has_sale'],
                 surname=None if 'surname' not in user else user['surname'],
                 address=user['address'],
                 coffee_id=random.choice(coffe_ids))
            for user in users]


def create_init_data(engine, session):
    # Если бд пустая - соберем ее
    if not inspect(engine).get_table_names():
        # Base.metadata.drop_all(engine)
        logger.info('В базе нет таблиц - соберем их')
        Base.metadata.create_all(engine)
    else:
        logger.info('БД уже создана')

    with session.begin():
        if not session.query(Coffee).first():
            logger.info('В таблице Coffee нет данных - начинаю загрузку рандомного кофе')
            objects = random_coffee()
            session.bulk_save_objects(objects)
            session.commit()
        else:
            count_records: int = session.query(func.count(Coffee.id)).scalar()
            logger.info(f'В таблице Coffee {count_records} записей')

    with session.begin():
        if not session.query(User).first():
            logger.info('В таблице User нет данных - начинаю загрузку рандомного пользователя')
            # Получим список id кофе
            coffee_idx: list = session.query(Coffee.id).all()
            coffee_idx = [row_with_id[0] for row_with_id in coffee_idx]
            objects = random_user(coffee_idx)
            session.bulk_save_objects(objects)
            session.commit()
        else:
            count_records: int = session.query(func.count(User.id)).scalar()
            logger.info(f'В таблице User {count_records} записей')
