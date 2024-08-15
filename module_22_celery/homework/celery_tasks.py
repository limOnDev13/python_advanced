"""
В этом файле будут Celery-задачи
"""
from celery import Celery, group
from celery.utils.log import get_task_logger
from celery.schedules import crontab

import os
from typing import Optional

from image import blur_image
from mail import send_email
from db import UserImages


celery_logger = get_task_logger('tasks_logger')
celery = Celery(
    __name__,
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)
database = UserImages()


@celery.task
def process_image(image_path: str) -> Optional[str]:
    """
    Функция - задача. Блюрит изображение и возвращает путь до полученного изображения
    :param image_path: Путь до изображения, которое нужно заблюрить. Пока на лок машине
    :return: Путь заблюренного изображения
    """
    try:
        celery_logger.debug(f'1) Before blur_image. image_path = {image_path}')
        blured_image_path: str = blur_image(image_path,
                                            f'./static/blured_images/{os.path.split(image_path)[1]}')
        celery_logger.debug(f'2) After blur_image. blured_image_path = {blured_image_path}')
        return blured_image_path
    except Exception as exc:
        celery_logger.exception('Exception in the blur_image function', exc_info=exc)


def process_group_images(images: list[str], receiver: Optional[str] = None) -> str:
    """
    Функция ставит в очередь обработку переданных изображений. Возвращает ID группы задач по обработке изображений.
    :param images: Список путей до изображений
    :param receiver: Почта получателя. Необязательный параметр
    :return: id группы задач
    """
    celery_logger.debug('Before creating a task group')
    task_group = group(process_image.s(image) for image in images)
    celery_logger.debug('Before apply_async()')
    group_result = task_group.apply_async()
    celery_logger.debug('Saving group')
    group_result.save()

    # Если был передан получатель - сохраним инфу в бд
    celery_logger.debug(f'receiver = {receiver}')
    if receiver:
        database.add(receiver, [group_result.id])

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
        celery_logger.warning(f'Group not found')


def _get_group_results(group_id: str) -> Optional[list[str]]:
    """Возвращает результаты задач из группы по ее id (список путей до обработанных изображений)"""
    group_result = celery.GroupResult.restore(group_id)

    if group_result:
        return [task_res.result for task_res in group_result]
    else:
        celery_logger.warning('Group not found')


@celery.task
def send_emails_to_all_receivers() -> None:
    """Функция получает список всех пользователей и отправляет им email с обработанными изображениями (если они есть).
    Для каждой отдельной группы изображений отправляется отдельное письмо"""
    # Получим данные о пользователях
    users_images: Optional[dict[str, list[str]]] = database.get()

    sending_tasks: list = list()
    # Если бд не пустая - отправим письма
    if users_images:
        for user, groups in users_images.items():
            celery_logger.debug(f'user: {user}; groups: {groups}')
            if groups:
                for group_id in groups:
                    celery_logger.debug(f'group_id: {group_id}')
                    images: Optional[list[str]] = _get_group_results(group_id)

                    send_email(receiver=user, order_id=group_id, images=images)
            else:
                send_email(user)

        # После отправки изображений пользователям можно удалить старые фотографии и очистить бд (email-ы останутся)
        database.clear()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # # Для тестирования - письмо будет отправляться каждые полторы минуты
    # celery_logger.info('Planning sending emails')
    # sender.add_periodic_task(60, send_emails_to_all_receivers.s())

    # Для конечной версии - письмо будет отправляться каждый понедельник в 18:30
    sender.add_periodic_task(
        crontab(hour='18', minute='30', day_of_week='1'),
        send_emails_to_all_receivers()
    )


@celery.task
def subscribe_user(email: str) -> bool:
    """Функция - задача. Подписывает пользователя на еженедельную подписку (просто добавляет в бд email)"""
    return database.add(email)


@celery.task
def unsubscribe_user(email: str) -> bool:
    """Функция - задача. Отписывает пользователя от еженедельной подписки (просто удаляет из бд email).
    Если пользователь был в бд - вернет True, иначе - False"""
    try:
        database.remove(email)
        return True
    except ValueError:
        return False
