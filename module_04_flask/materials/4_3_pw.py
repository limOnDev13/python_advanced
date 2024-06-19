"""Практическая работа 4.3"""
import json
from flask import Flask, request


app: Flask = Flask(__name__)


def calc_shift_array(nums: list[int]) -> tuple[int, list[int]]:
    """
    Функция получает сдвинутый отсортированный массив, находит сдвиг и сдвигает массив
    :param nums: Сдвинутый отсортированный массив чисел
    :type nums: list[int]
    :return: Сдвиг и отсортированный массив
    :rtype: tuple[int, list[int]]
    """
    # 1) Смотрим сдвиг
    shift: int = nums.index(max(nums))
    direction: int = 1  # правое направление
    if shift == 0:
        shift = nums.index(min(nums))
        direction = -1  # левое направление

    # 2) Смотрим, в какую сторону сдвигать лучше всего
    if len(nums) - shift < shift:
        shift = len(nums) - shift
        direction *= -1

    # 3) Сдвигаем массив. Можно просто отсортировать исходный массив, но для проверки лучше вручную сдвинуть его
    return shift, nums[-direction * shift:] + nums[:-direction * shift]


@app.route('/calc_shift', methods=['POST'])
def calc_shift() -> tuple[str, int]:
    """Функция - эндпоинт. С помощью POST запроса получает отсортированный массив чисел со сдвигом в формате json
     (по ключу 'nums'), находит сдвиг и возвращает сдвиг и правильный массив"""
    form_data = request.get_data(as_text=True)
    data = json.loads(form_data)

    shift, sort_nums = calc_shift_array(data['nums'])

    return f'Массив {sort_nums} сдвинут на {shift}', 200


if __name__ == '__main__':
    app.run(debug=True)
