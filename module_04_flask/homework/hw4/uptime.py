"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""

from flask import Flask
from sh import Command
from typing import Optional


app = Flask(__name__)


@app.route("/uptime", methods=['GET'])
def uptime() -> tuple[str, int]:
    """
    Функция - эндпоинт. По запросу возвращает uptime системы
    :return:
    """
    uptime_command: Command = Command('uptime')
    uptime_result: list[str] = list()  # здесь будут храниться строки результата работы upotime

    def save_result(result) -> None:
        """Функция получает построчно результат команды uptime и сохраняет его"""
        nonlocal uptime_result
        uptime_result.append(result)

    uptime_command('-p', _out=save_result)

    return f'<pre>{"<br>".join(uptime_result)}</pre>', 200


if __name__ == '__main__':
    app.run(debug=True)
