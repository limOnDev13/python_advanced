from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import func
import logging

from module_27_postgres_migrations.hw import app, session
from models import User, Coffee
from schemas import UserSchema


logger = logging.getLogger('init_logger.routes_logger')
logger.setLevel(logging.INFO)


@app.route('/users', methods=['POST'])
def add_user():
    """""Эндпоинт для добавления нового пользователя"""
    data = request.json

    schema = UserSchema()

    try:
        user = schema.load(data)
        session.add(user)
        session.commit()
        return jsonify(message='OK', user=user.to_json()), 201
    except ValidationError as exc:
        return jsonify(message='ValidationError', exc_info=exc)


@app.route('/users', methods=['GET'])
def get_all_users():
    """Эндпоинт для получения списка всех пользователей"""
    users: list[User] = session.query(User).all()
    return jsonify(users=[user.to_json() for user in users]), 200


@app.route('/coffee/<title>', methods=['GET'])
def get_coffee_by_title(title: str):
    """Эндпоинт делает полнотекстовый поиск по названию кофе и возвращает список"""
    coffee_list = session.query(Coffee).filter(func.to_tsvector(Coffee.title).match(title)).all()
    return jsonify(coffee_list=[coffee.to_json() for coffee in coffee_list]), 200


@app.route('/coffee', methods=['GET'])
def get_list_coffee():
    """Эндпоинт возвращает список кофе из бд"""
    coffee_list = session.query(Coffee).all()
    return jsonify(coffee_list=[coffee.to_json() for coffee in coffee_list]), 200


@app.route('/unique_notes', methods=['GET'])
def get_unique_coffee():
    """Эндпоинт возвращает список уникальных элементов в заметках к кофе"""
    notes_tuples: list[tuple[str]] = session.query(Coffee.notes).all()
    logger.debug(f'Получены заметки: {notes_tuples}')
    elements_in_notes: set[str] = set()

    for note in notes_tuples:
        logger.debug(f'Обработка заметки {note}')
        set_elements: set = set(note[0].split(', '))
        logger.debug(f'Заметка разделена на элементы {set_elements}')
        elements_in_notes = elements_in_notes.union(set(note[0].split(', ')))
        logger.debug(f'Элементы объедены, текущее множество {elements_in_notes}')

    return jsonify(unique_elements_in_notes=list(elements_in_notes)), 200


@app.route('/users/<country>', methods=['GET'])
def get_list_users_in_country(country: str):
    """Эндпоинт возвращает список пользователей из указанной страны"""
    users = session.query(User).filter(User.address['country'].as_string().like(f'{country}%')).all()
    return jsonify(country=country, users=[user.to_json() for user in users]), 200


if __name__ == '__main__':
    app.run(debug=True)
