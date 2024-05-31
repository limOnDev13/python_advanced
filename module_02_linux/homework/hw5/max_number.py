"""
Реализуйте endpoint, начинающийся с /max_number, в который можно передать список чисел, разделённых слешем /.
Endpoint должен вернуть текст «Максимальное переданное число {number}»,
где number — выделенное курсивом наибольшее из переданных чисел.

Примеры:

/max_number/10/2/9/1
Максимальное число: 10

/max_number/1/1/1/1/1/1/1/2
Максимальное число: 2

"""

from flask import Flask

app = Flask(__name__)


@app.route("/max_number/<path:numbers>")
def max_number(numbers: str) -> tuple[str, int]:
    """
    Функция - эндпоинт. Выводит максимальное число из url
    :param numbers: url, который содержит числа, разделенные '/'. Если введено что-то, кроме чисел,
    сообщает об этом пользователю и выдает статус код 400
    :type numbers: str
    :return: Выводит максимальное число
    :rtype: tuple[str, int]
    """
    try:
        nums: list[float] = [float(num) for num in numbers.split('/')]

        return str(max(nums)), 200
    except ValueError:
        return 'Введите числа через / чтобы увидеть максимальное', 400


if __name__ == "__main__":
    app.run(debug=True)
