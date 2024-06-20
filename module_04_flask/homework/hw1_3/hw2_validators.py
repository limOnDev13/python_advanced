"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""
from typing import Optional, Callable

from flask_wtf import FlaskForm
from wtforms import Field, ValidationError


def number_length(min: int, max: int, message: Optional[str] = None) -> Callable:
    """
    Функция - валидатор для проверки корректности номера телефона
    :param min: Минимальная длина номера
    :type min: int
    :param max: Максимальная длина номера
    :type max: int
    :param message: Сообщение в случае ошибки валидации
    :type message: Optional[str]
    :return: None
    """
    if not message:
        message = f'Длина числа должна находится в диапазоне [{min}, {max}]!'

    def number_length_wrapper(form: FlaskForm, field: Field) -> None:
        """
        Оборачиваемя функция валидатор.
        :param form: Flask форма
        :type form: FlaskForm
        :param field: Поле формы
        :type field: Field
        :return: None
        """
        if not min <= len(str(field.data)) <= max:
            raise ValidationError(message)

    return number_length_wrapper


class NumberLength:
    """
    Класс - валидатор для проверки корректности длины номера телефона
    Args:
        min (int) - минимальная длина номера
        max (int) - максимальная длина номера
        message (Optional[str]) - сообщение ошибки валидации
    """
    def __init__(self, min: int, max: int, message: Optional[str] = None):
        self.__min: int = min
        self.__max: int = max
        if not message:
            self.__msg: str = f'Длина числа должна находится в диапазоне [{min}, {max}]!'
        else:
            self.__msg: str = message

    def __call__(self, form: FlaskForm, field: Field) -> None:
        if not self.__min <= len(str(field.data)) <= self.__max:
            raise ValidationError(self.__msg)
