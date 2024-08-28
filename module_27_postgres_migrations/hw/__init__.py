from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
from typing import List
import time
import logging

from .models import Base, User, Coffee



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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
            coffee_list.append(coffee)
            time.sleep(2)  # Задержка, чтобы избежать 429 кода ответа
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


def random_user(num_users: int = 10) -> List[User]:
    """Функция возвращает словарь с генерированными пользователями"""
    users: List[User] = list()
    idx: int = 0

    while len(users) < num_users:
        try:
            logger.debug(f'{idx} попытка получения рандомного пользователя')
            user = requests.get(RANDOM_USER_URL).json()
            address = requests.get(RANDOM_ADDRESS_URL).json()
            user['address'] = address
            users.append(user)
            idx += 1
            time.sleep(2)
        except Exception as exc:
            logger.exception('Попытка провалилась', exc_info=exc)
        else:
            logger.debug('Попытка успешная')

    return [User(name=user['name'], has_sale=user['has_sale'], address=user['address'], coffee_id=coffee_id)
            for coffee_id, user in enumerate(users)]


# Base.metadata.drop_all(engine)
logger.debug('До Base.metadata.create_all(engine)')
Base.metadata.create_all(engine)
logger.debug('После Base.metadata.create_all(engine)')

if not session.query(Coffee).first():
    logger.debug('В таблице Coffee нет данных - начинаю загрузку рандомного кофе')
    objects = random_coffee()
    session.bulk_save_objects(objects)
    session.commit()

if not session.query(User).first():
    logger.debug('В таблице User нет данных - начинаю загрузку рандомного пользователя')
    objects = random_user()
    session.bulk_save_objects(objects)
    session.commit()
