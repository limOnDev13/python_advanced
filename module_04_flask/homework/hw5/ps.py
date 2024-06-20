"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""

from flask import Flask, request
from sh import Command, ErrorReturnCode
from typing import Optional

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> tuple[str, int]:
    """Функция - эндпоинт. Получает список аргументов для командной строки и возвращает результат работы команды
     ps с этими аргументами"""
    args: list[str] = request.args.getlist('arg')

    try:
        ps_cmd: Command = Command('ps')
        ps_result: list[str] = list()

        def save_result(result) -> None:
            """Костыль. Пробовал сделать конвейер сразу в переменную uptime_result, но не получилось"""
            nonlocal ps_result
            ps_result.append(result)

        ps_cmd(*args, _out=save_result)

        return f'<pre>{"<br>".join(ps_result)}</pre>', 200
    except ErrorReturnCode:
        return 'Переданы неправильные параметры!', 400


if __name__ == "__main__":
    app.run(debug=True)
