"""
Здесь происходит логика обработки изображения
"""

from typing import Optional

from PIL import Image, ImageFilter


def blur_image(src_filename: str, dst_filename: Optional[str] = None) -> str:
    """
    Функция принимает на вход имя входного и выходного файлов.
    Применяет размытие по Гауссу со значением 5. Возвращает путь заблюренного изображения
    """
    if not dst_filename:
        dst_filename = f'blur_{src_filename}'
        print(dst_filename)

    with Image.open(src_filename) as img:
        print('image load')
        img.load()
        print('filter image')
        new_img = img.filter(ImageFilter.GaussianBlur(5))
        print('Saving image')
        new_img.save(dst_filename)
        print('return')

    return dst_filename


if __name__ == '__main__':
    print(blur_image('./static/images/2.png', './static/blured_images/blur_2.png'))
