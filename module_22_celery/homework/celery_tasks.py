"""
В этом файле будут Celery-задачи
"""
from celery import Celery, group
import os
import logging
from typing import Optional

from image import blur_image
from mail import send_email
from config.config import MailConfig


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


@celery.task
def process_sending_email(group_id: str, receiver: str, image: str, mail_config: MailConfig) -> None:
    send_email(group_id, receiver, )


def process_group_images(images: list[str]) -> str:
    """
    Функция ставит в очередь обработку переданных изображений. Возвращает ID группы задач по обработке изображений.
    :param images: Список путей до изображений
    :return: id группы задач
    """
    celery_logger.debug('Before creating a task group')
    task_group = group(process_image.s(image) for image in images)
    celery_logger.debug('Before apply_async()')
    group_result = task_group.apply_async()
    celery_logger.debug('Saving group')
    group_result.save()

    return group_result.id


def get_group_info(group_id: str) -> Optional[tuple[str, list[str]]]:
    """
    Функция возвращает количество выполненных задач в группе и статусы каждой задач
    :param group_id: id группы
    :return: Количество выполненных задач - строка вида <кол-во выполненных задач>/<кол-во задач> и
    список статусов каждой задачи
    """
    celery_logger.debug('Before GroupResult.restore()')
    group_result = celery.GroupResult.restore(group_id)

    if group_result:
        num_comp_tasks: str = f'{group_result.completed_count()}/{len(group_result)}'
        celery_logger.debug(f'Number of completed tasks = {num_comp_tasks}')
        statuses: list[str] = [result.status for result in group_result]
        celery_logger.debug(f'Tasks statuses = {statuses}')

        return num_comp_tasks, statuses
    else:
        celery_logger.debug(f'Group not found')


def run_celery() -> None:
    celery.conf.update(worker_pool_restarts=True)
    celery.worker_main(['worker', '-B'])
