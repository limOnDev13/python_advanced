"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""
import subprocess
from subprocess import TimeoutExpired
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired
from typing import Any
from subprocess import Popen
import shlex

app = Flask(__name__)


class CodeForm(FlaskForm):
    code = StringField(validators=[InputRequired()])
    timeout = IntegerField(validators=[InputRequired()])


def run_python_code_in_subprocess(code: str, timeout: int) -> tuple[str, int]:
    """
    Функция выполняет полученный python код в отдельном процессе. Функция выводит ТОЛЬКО stdout и stderr.
    Если код что-то возвращает, но не выводит в stdout, то и функция ничего не вернет.
    Если выполнение кода занимает больше времени, чем timeout, то выбрасывается исключение.
    :param code: python code
    :type code: str
    :param timeout: таймаут в секундах
    :type timeout: int
    :return: Результат работы кода в строковом виде и статус кода
    :rtype: tuple[str, int]
    """
    command_line: str = f'prlimit --nproc=1:1 python -c "{code}" >1'
    command: list[str] = shlex.split(command_line)

    try:
        proc: Popen = Popen(command, stdout=subprocess.PIPE)
        proc_res: Any = proc.communicate(timeout=timeout)
        result: str = proc_res[0].decode()
        return result, 200
    except TimeoutExpired:
        return 'Исполнение кода не уложилось в данное время', 400
    finally:
        proc.stdout.close()


@app.route('/run_code', methods=['POST'])
def run_code() -> tuple[str, int]:
    """Функция - эндпоинт. С помощью POST запроса получает python код и timeout, и возвращает результат
    выполнения этого кода. Если не верен input, выполнение коды вызвало ошибку или превысило timeout -
    вернет 400 status code"""
    form: CodeForm = CodeForm()

    if form.validate_on_submit():
        code, timeout = form.code.data, form.timeout.data
        return run_python_code_in_subprocess(code, timeout)
    return f'Invalid input, {form.errors}', 499


if __name__ == '__main__':
    # app.config['WTF_CSRF_ENABLED'] = False
    # app.run(debug=True)
    code: str = ("from subprocess import run\n"
                 "run(['./kill_the_system.sh'])")
    print(run_python_code_in_subprocess(code, 1000))
