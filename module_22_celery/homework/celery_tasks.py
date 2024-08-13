"""
В этом файле будут Celery-задачи
"""
from celery import Celery, group
import os

from image import blur_image


celery = Celery(
    __name__,
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)


@celery.task
def process_image(image_path: str):
    """
    Функция - задача. Блюрит изображение и возвращает путь до полученного изображения
    :param image_path: Путь до изображения, которое нужно заблюрить. Пока на лок машине
    :return: Путь заблюренного изображения
    """
    print('before blur_image')
    blured_image_path: str = blur_image(image_path, f'./static/blured_images/blur_{os.path.split(image_path)[1]}')
    print('after blur_image')
    return blured_image_path


def process_group_images(images: list[str]) -> str:
    """
    Функция ставит в очередь обработку переданных изображений. Возвращает ID группы задач по обработке изображений.
    :param images: Список путей до изображений
    :return: id группы задач
    """
    task_group = group(process_image.s(image) for image in images)
    group_result = task_group.apply_async()

    if group_result.successful():
        group_result.save()
    else:
        print('Ошибка!')
        for result in group_result.results:
            print(result.status)

    return group_result.id
