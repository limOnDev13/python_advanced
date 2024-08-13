import random
from celery import Celery
from celery.app.control import Inspect
import time


# Конфигурация Celery
celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)
inspect = Inspect(app=celery)


# Задача Celery для обработки изображения
@celery.task
def process_image(image_id):
    # В реальной ситуации здесь может быть обработка изображения
    # В данном примере просто делаем задержку для демонстрации
    time.sleep(random.randint(5, 15))
    return f'Image {image_id} processed'


@celery.task
def control_tasks_and_queues():
    """Функция собирает информацию о задачах и очередях, которые выполняются на воркерах"""
    current_info: dict = dict()
    current_info['tasks_info'] = inspect.active()
    current_info['queues_info'] = inspect.active_queues()
    return current_info


@celery.on_after_configure.connect
def setup_periodic_task(sender, **kwargs):
    """Функция задает периодическое выполнение задачи"""
    sender.add_periodic_task(10, control_tasks_and_queues.s())
