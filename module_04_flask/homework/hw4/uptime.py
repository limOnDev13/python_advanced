"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""

from flask import Flask
import subprocess
from subprocess import CompletedProcess
import shlex


app = Flask(__name__)


@app.route("/uptime", methods=['GET'])
def _uptime() -> tuple[str, int]:
    """
    Функция - эндпоинт. По запросу возвращает uptime системы
    :return:
    """
    command_str: str = 'uptime -p'
    command: list[str] = shlex.split(command_str)
    uptime: CompletedProcess = subprocess.run(command, capture_output=True)
    time: str = uptime.stdout.decode().lstrip('up ')
    return f'Время работы системы: {time}', 200


if __name__ == '__main__':
    app.run(debug=True)
