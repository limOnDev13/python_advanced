"""
Здесь происходит логика обработки изображения
"""
from typing import Optional
from PIL import Image, ImageFilter
import logging


image_logger = logging.getLogger('image_logger')


def blur_image(src_filename: str, dst_filename: Optional[str] = None) -> str:
    """
    Функция принимает на вход имя входного и выходного файлов.
    Применяет размытие по Гауссу со значением 5. Возвращает путь заблюренного изображения
    """
    if not dst_filename:
        dst_filename = f'blur_{src_filename}'
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
    print(blur_image('./static/images/2.png', './static/blured_images/blur_2.png'))
