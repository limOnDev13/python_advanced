"""
В этом файле будет ваше Flask-приложение
"""
from flask import Flask, request, jsonify

from celery_tasks import process_group_images


app = Flask(__name__)


@app.route('/blur', methods=['POST'])
def process_images():
    """Функция - эндпоинт. Ставит в очередь обработку переданных изображений.
     Возвращает ID группы задач по обработке изображений."""
    images = request.json.get('images')

    if images and isinstance(images, list):
        return jsonify({'group_id': process_group_images(images)})
    else:
        return jsonify({'error': 'Missing or invalid images params'}), 400


if __name__ == '__main__':
    app.run(debug=True)
