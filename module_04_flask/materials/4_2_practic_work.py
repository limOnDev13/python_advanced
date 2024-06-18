"""Практическая работа 4.2"""

from flask import Flask, request
from typing import Optional
from datetime import date, datetime


app: Flask = Flask(__name__)


def check_date(date_str: str) -> None:
    """
    Метод проверяет корректность даты. Дата не должна быть в будущем
    :param date_str: Дата (строка) в формате YYYYMMDD
    :raise IOError: Если дата имеет неверный формат или она в будущем
    :return: None
    """
    if len(date_str) != 8:
        raise IOError('Неверный формат даты! Длина строки даты должна быть равной 8!')

    try:
        year: int = int(date_str[:4])
        month: int = int(date_str[4:6])
        day: int = int(date_str[6:])
        correct_date: datetime = datetime(year, month, day)
    except ValueError:
        raise IOError('Неверный формат даты! Дата должна иметь формат YYYYMMDD!')

    if correct_date > datetime.now():
        raise IOError('Дата не должна быть в будущем!')


@app.route('/search/', methods=['GET'])
def search() -> tuple[str, int]:
    cell_tower_ids: list[int] = request.args.getlist('cell_tower_id', type=int)
    if not cell_tower_ids:
        return 'You must specify at least one cell_tower_id', 400
    for cell_tower_id in cell_tower_ids:
        if cell_tower_id <= 0:
            return f'cell_tower_id должен быть больше 0!', 400

    phone_prefixes: list[str] = request.args.getlist('phone_prefix', type=str)
    for prefix in phone_prefixes:
        if prefix[-1] != '*':
            return 'phone_prefix должен оканчиваться на *!', 400
        if len(prefix) - 1 > 10:
            return 'phone_prefix должен иметь не больше 10 цифр!', 400
        if not prefix[:-1].isdigit():
            return 'phone_prefix должен состоять из цифр и оканчиваться *!', 400

    protocols: list[str] = request.args.getlist('protocol')
    if not set(protocols).issubset({'2G', '3G', '4G'}):
        return 'protocol должен быть 2G, 3G или 4G!', 400

    signal_level: Optional[float] = request.args.get('signal_level', type=float, default=None)
    date_from: Optional[str] = request.args.get('date_from', type=str, default=None)
    date_to: Optional[str] = request.args.get('date_to', type=str, default=None)
    try:
        if date_from:
            check_date(date_from)
        if date_to:
            check_date(date_to)

        if date_to and date_from:
            if (date(int(date_from[:4]), int(date_from[4:6]), int(date_from[6:])) >=
                    date(int(date_to[:4]), int(date_to[4:6]), int(date_to[6:]))):
                raise IOError('date_to всегда должна быть больше чем date_from!')
    except IOError as exc:
        return exc.__str__(), 400

    return (f'Переданные значение через GET запрос:<br>'
            f'cell_tower_ids = {cell_tower_ids}<br>'
            f'phone_prefixes = {phone_prefixes}<br>'
            f'protocols = {protocols}<br>'
            f'signal_level = {signal_level}<br>'
            f'date_from = {date_from}<br>'
            f'date_to = {date_to}'), 200


@app.route('/sum_nums/', methods=['GET'])
def sum_nums() -> tuple[str, int]:
    """
    Функция - эндпоинт. Принимает массив чисел и возвращает их сумму и произведение
    :return: response
    """
    nums: list[float] = request.args.getlist('num', type=float)

    res_sum: float = sum(nums)
    res_product: float = 1
    for num in nums:
        res_product *= num

    return f'Сумма чисел: {res_sum}<br>Произведение чисел: {res_product}', 200


@app.route('/all_combo/', methods=['GET'])
def all_combo() -> tuple[str, int]:
    """Функция - эндпоинт. Возвращает все возможные комбинации пар чисел из двух массивов"""
    list1: list[float] = request.args.getlist('list1', type=float)
    list2: list[float] = request.args.getlist('list2', type=float)

    result_list: list[tuple[float, float]] = [(num1, num2)
                                              for num1 in list1
                                              for num2 in list2]

    return f'Всевозможные комбинации:<br>{result_list}', 200


@app.route('/nearest_num/', methods=['Get'])
def nearest_num() -> tuple[str, int]:
    """Функция - эндпоинт. Принимает отсортированный (по возрастанию) массив чисел и целевое число
     и возвращает число из массива, наиболее близкое к целевому"""
    nums: list[float] = request.args.getlist('num', type=float)
    target: float = request.args.get('target', type=float)

    res_num: float = nums[0]

    if target > nums[-1]:
        res_num = nums[-1]
    elif nums[0] < target < nums[-1]:
        prev_num: float = nums[0]
        for num in nums:
            if prev_num <= target <= num:
                if abs(target - prev_num) < abs(target - num):
                    res_num = prev_num
                else:
                    res_num = num
                break
            else:
                prev_num = num

    return f'Максимально близкое число к целевому: {res_num}', 200


if __name__ == '__main__':
    app.run(debug=True)
