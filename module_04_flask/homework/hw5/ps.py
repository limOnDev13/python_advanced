"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""

from flask import Flask, request
import subprocess
from subprocess import CompletedProcess
import shlex

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def _ps() -> tuple[str, int]:
    """Функция - эндпоинт. Получает список аргументов для командной строки и возвращает результат работы команды
     ps с этими аргументами"""
    args: list[str] = request.args.getlist('arg')

    command_str: str = 'ps ' + ' '.join(shlex.quote(arg) for arg in args)
    command: list[str] = shlex.split(command_str)
    ps: CompletedProcess = subprocess.run(command, capture_output=True)
    processes: str = ps.stdout.decode()
    return f'<pre>{processes}</pre>', 200


if __name__ == "__main__":
    app.run(debug=True)
