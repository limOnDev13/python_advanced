"""
В этом файле будет ваше Flask-приложение
"""
from flask import Flask, request, jsonify
import logging.config

from celery_tasks import process_group_images
from logging_config import dict_config


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


if __name__ == '__main__':
    app.run(debug=True)
