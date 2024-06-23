"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""
import subprocess

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from typing import Any
from subprocess import Popen
import shlex

app = Flask(__name__)


class CodeForm(FlaskForm):
    code = StringField()
    timeout = IntegerField()


def run_python_code_in_subprocess(code: str, timeout: int) -> Any:
    """
    Функция выполняет полученный python код в отдельном процессе. Если выполнение кода занимает больше времени,
    чем timeout, то выбрасывается исключение.
    :param code: python code
    :type code: str
    :param timeout: таймаут в секундах
    :type timeout: int
    :return: Результат работы кода
    :rtype: Any
    """
    command_line: str = f'prlimit --nproc=1:1 python -c "{code}"'
    command: list[str] = shlex.split(command_line)
    print(command)
    proc: Popen = Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc_res: Any = proc.communicate(timeout=timeout)
    return proc_res


@app.route('/run_code', methods=['POST'])
def run_code() -> tuple[str, int]:
    """Функция - эндпоинт. С помощью POST запроса получает python код и timeout, и возвращает результат
    выполнения этого кода. Если не верен input, выполнение коды вызвало ошибку или превысило timeout -
    вернет 400 status code"""
    form: CodeForm = CodeForm()

    if form.validate_on_submit():
        code, timeout = form.code.data, form.timeout.data
        result: Any = run_python_code_in_subprocess(code, timeout)
        result = [item.decode() for item in result]

        return ''.join(result), 200
    return f'Invalid input, {form.errors}', 400


if __name__ == '__main__':
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
