"""
Здесь происходит логика обработки изображения
"""
from typing import Optional
from PIL import Image, ImageFilter
import logging
import os
import re


image_logger = logging.getLogger('utils_logger')


def _unique_dst_filename(dst_filename: str) -> str:
    """Функция возвращает уникальное имя файла (чтобы решить проблему с одинаковыми именами)"""
    # Пока мы не найдем уникальное название, будем его менять
    while os.path.exists(dst_filename):
        image_logger.debug(f'Current filename path: {dst_filename}')
        # Разделим путь по '.', чтобы найти название файла
        filename_parts: list[str] = dst_filename.split('.')
        # Названием файла будет предпоследняя строка.
        # В директории может быть несколько файлов с названиями типа filename(1).jpg.
        # Найдем число, которое еще не использовалось в скобках в названии
        image_logger.debug(f'Current filename {filename_parts[-2]}')
        match: re.Match = re.search(r'\((\d+)\)$', filename_parts[-2])
        if match:
            counter: int = int(match.group()[1:-1])
            image_logger.debug(f'Number in filename: {counter}')
            # Если нашли такое название - увеличим число на 1
            filename_parts[-2] = re.sub(fr'\({counter}\)$', f'({counter + 1})', filename_parts[-2])
        else:
            # Если названий с числом в скобках не нашли - начнем с 1
            filename_parts[-2] += '(1)'

        dst_filename = '.'.join(filename_parts)

    image_logger.debug(f'Result dst_file_name: {dst_filename}')
    return dst_filename


def blur_image(src_filename: str, dst_filename: Optional[str] = None) -> str:
    """
    Функция принимает на вход имя входного и выходного файлов.
    Применяет размытие по Гауссу со значением 5. Возвращает путь заблюренного изображения
    """
    if not dst_filename:
        dst_filename = f'./static/blured_images/{src_filename.split(os.path.sep)[-1]}'
    dst_filename = _unique_dst_filename(dst_filename)
    image_logger.debug(f'1) src_filename = {src_filename}; dst_filename = {dst_filename}')

    try:
        image_logger.debug(f'2) Opening {src_filename}')
        with Image.open(src_filename) as img:
            image_logger.debug('3) Loading image')
            img.load()
            image_logger.debug('4) Blurring image')
            new_img = img.filter(ImageFilter.GaussianBlur(5))
            image_logger.debug('5) Saving new image')
            new_img.save(dst_filename)

        return dst_filename
    except Exception as exc:
        image_logger.exception('Exception during processing image', exc_info=exc)


if __name__ == '__main__':
    print(blur_image('./static/images/2.png'))
    print(blur_image('./static/images/2.png'))
    print(blur_image('./static/images/2.png'))
