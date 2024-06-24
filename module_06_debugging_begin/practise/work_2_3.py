"""
Напишите Flask POST endpoint /calculate,
который принимает на вход арифметическое выражение и
вычисляет его с помощью eval (о безопасности думать не нужно,
работайте только над фукнционалом).

Поскольку наш Flask endpoint работает с арифметическими выражениями,
напишите 4 error_handler-а, которые будет обрабатывать
ArithmeticError, ZeroDivisionError, FloatingPointError и OverflowError
(о значении этих исключений вы можете посмотреть
вот на этой страничке https://docs.python.org/3/library/exceptions.html ).

Напишите по unit-тесту на каждую ошибку: тест должен проверять, что ошибка обрабатывается

Примечание: рекомендуется обрабатывать  ArithmeticError,
перехватывая InternalServerError ,
остальные классы ошибок можно обрабатывать напрямую.
"""
from werkzeug.exceptions import InternalServerError
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
from typing import Optional


class FormulaForm(FlaskForm):
    formula = StringField(validators=[InputRequired()])


app: Flask = Flask(__name__)


@app.route('/calculate', methods=['POST'])
def calculate() -> tuple[str, int]:
    """Функция - ендпоинт. Выполняет арифметическую формулу, переданную через POST запрос"""
    form: FormulaForm = FormulaForm()

    if form.validate_on_submit():
        result: str = eval(form.formula.data)
        return f'Результат выполнения: {result}', 200
    return f'Invalid input', 400


def write_message(message: str, file_name: str = 'invalid_error.log'):
    """
    Функция записывает сообщение в файл
    :param message: Сообщение
    :type message: str
    :param file_name: Имя файла
    :type file_name: str
    :return: None
    """
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write(message)


@app.errorhandler(InternalServerError)
def handle_exception(exc: InternalServerError) -> tuple[str, int]:
    original: Optional[Exception] = getattr(exc, "original_exception", None)

    if isinstance(original, ZeroDivisionError):
        raise ZeroDivisionError('На ноль делить нельзя!')
    elif isinstance(original, FloatingPointError):
        raise exc
    elif isinstance(original, OverflowError):
        raise exc
    elif isinstance(original, ArithmeticError):
        raise exc

    return 'Internal server error', 500


if __name__ == "__main__":
    # app.config['DEBUG'] = True
    # app.run()
    print()
