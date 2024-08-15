"""
В этом файле будет ваше Flask-приложение
"""
from flask import Flask, request, jsonify
import logging.config
from typing import Optional

from celery_tasks import process_group_images, get_group_info, subscribe_user
from config.logging_config import dict_config


app = Flask(__name__)
logging.config.dictConfig(dict_config)
app_logger = logging.getLogger('app_logger')


@app.route('/blur', methods=['POST'])
def process_images():
    """Функция - эндпоинт. Ставит в очередь обработку переданных изображений.
     Возвращает ID группы задач по обработке изображений. Если передан email - добавляет в рассылку"""
    images = request.json.get('images')
    receiver = request.json.get('email')

    if images and isinstance(images, list):
        app_logger.info('images have been received')
        return jsonify({'group_id': process_group_images(images, receiver)})
    else:
        app_logger.info('Endpoint /blur - missing or invalid images params')
        return jsonify({'error': 'Missing or invalid images params'}), 400


@app.route('/status/<group_id>', methods=['GET'])
def get_status(group_id: str):
    """Функция - эндппоинт. Возвращает информацию о задаче: прогресс (количество обработанных задач)
    и статус (в процессе обработки, обработано)."""
    app_logger.info('Getting info about group by id')
    group_info: Optional[tuple[str, list[str]]] = get_group_info(group_id)

    if group_info:
        return jsonify(number_completed_tasks=group_info[0], statuses=group_info[1]), 200
    else:
        app_logger.info('Group not found')
        return jsonify(error='Group not found'), 404


@app.route('/subscribe', methods=['POST'])
def subscribe():
    """Функция - эндпоинт. Пользователь указывает почту и подписывается на рассылку.
    Каждую неделю ему будет приходить письмо о сервисе на почту."""
    app_logger.info('Subscribing user')
    email = request.json.get('email')

    if email and isinstance(email, str):
        result = subscribe_user.delay(email)
        if result.get():
            return jsonify(status='A user with such an email has already subscribed to the newsletter'), 200
        else:
            return jsonify(status='The subscription has been successfully completed'), 201
    return jsonify(status='The "email" field must be filled in'), 400


if __name__ == '__main__':
    app.run(debug=True)
