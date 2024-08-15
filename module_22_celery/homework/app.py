"""
В этом файле будет ваше Flask-приложение
"""
from flask import Flask, request, jsonify
import logging.config
from typing import Optional

from celery_tasks import process_group_images, get_group_info
from module_22_celery.homework.config.logging_config import dict_config


app = Flask(__name__)
logging.config.dictConfig(dict_config)
app_logger = logging.getLogger('app_logger')


@app.route('/blur', methods=['POST'])
def process_images():
    """Функция - эндпоинт. Ставит в очередь обработку переданных изображений.
     Возвращает ID группы задач по обработке изображений."""
    images = request.json.get('images')

    if images and isinstance(images, list):
        app_logger.info('Endpoint /blur - images have been received')
        return jsonify({'group_id': process_group_images(images)})
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


if __name__ == '__main__':
    app.run(debug=True)
