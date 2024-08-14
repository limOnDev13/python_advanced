"""
В этом файле будут Celery-задачи
"""
from celery import Celery, group
import os
import logging
from typing import Optional

from image import blur_image


celery_logger = logging.getLogger('tasks_logger')
celery = Celery(
    __name__,
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)


@celery.task
def process_image(image_path: str) -> Optional[str]:
    """
    Функция - задача. Блюрит изображение и возвращает путь до полученного изображения
    :param image_path: Путь до изображения, которое нужно заблюрить. Пока на лок машине
    :return: Путь заблюренного изображения
    """
    try:
        celery_logger.debug(f'1) Before blur_image. image_path = {image_path}')
        blured_image_path: str = blur_image(image_path, f'./static/blured_images/blur_{os.path.split(image_path)[1]}')
        celery_logger.debug(f'2) After blur_image. blured_image_path = {blured_image_path}')
        return blured_image_path
    except Exception as exc:
        celery_logger.exception('Exception in the blur_image function', exc_info=exc)
        return None


def process_group_images(images: list[str]) -> str:
    """
    Функция ставит в очередь обработку переданных изображений. Возвращает ID группы задач по обработке изображений.
    :param images: Список путей до изображений
    :return: id группы задач
    """
    celery_logger.debug('1) Before creating a task group')
    task_group = group(process_image.s(image) for image in images)
    celery_logger.debug('2) Before apply_async()')
    group_result = task_group.apply_async()

    try:
        celery_logger.debug('3) Get the results of each task from the group')
        results = group_result.get()
        celery_logger.debug(f'4.1) Results: {results}')
        celery_logger.debug(f'4.2) Statuses of results: {[result.status for result in group_result.results]}')
    except Exception as exc:
        celery_logger.exception('Exception when receiving the results of a task group', exc_info=exc)
    finally:
        return group_result.id
