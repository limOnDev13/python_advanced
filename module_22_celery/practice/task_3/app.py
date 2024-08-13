from flask import Flask, request, jsonify
from celery import group

from tasks import process_image, celery, control_tasks_and_queues


app = Flask(__name__)


@app.route('/process_images', methods=['POST'])
def process_images():
    images = request.json.get('images')

    if images and isinstance(images, list):
        # Создаем группу задач
        task_group = group(
            process_image.s(image_id)
            for image_id in images
        )

        # Запускаем группу задач и сохраняем ее
        result = task_group.apply_async()
        result.save()

        # Возвращаем пользователю ID группы для отслеживания
        return jsonify({'group_id': result.id}), 202
    else:
        return jsonify({'error': 'Missing or invalid images parameter'}), 400


@app.route('/status/<group_id>', methods=['GET'])
def get_group_status(group_id):
    result = celery.GroupResult.restore(group_id)

    if result:
        # Если группа с таким ID существует,
        # возвращаем долю выполненных задач
        status = result.completed_count() / len(result)
        return jsonify({'status': status}), 200
    else:
        # Иначе возвращаем ошибку
        return jsonify({'error': 'Invalid group_id'}), 404


@app.route('/cancel/<group_id>', methods=['GET'])
def cancel_group(group_id):
    """Функция - эндпоинт для отмены группы задач"""
    result = celery.GroupResult.restore(group_id)

    if result:
        result.revoke()
        return jsonify({'status': 'group canceled'}), 200
    else:
        return jsonify({'error': 'Invalid group_id'}), 404


@app.route('/control', methods=['GET'])
def control_tasks():
    """Функция возвращает информацию о задачах. Информация обновляется раз в 10 сек"""
    result = control_tasks_and_queues.delay()
    return jsonify({'info': result.get()}), 200


if __name__ == '__main__':
    app.run(debug=True)
