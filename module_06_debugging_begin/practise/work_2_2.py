"""
Посмотрите на приложение bank_api, который получился у нас на уроке.
Обратите внимание, сообщения у нас пишутся очень похоже друг на друга --
открываем файл на append, пишем сообщение, файл закрываем.

Это не дело, давайте не будем дублировать код.

Вынесите код записи сообщения в отдельную фукнцию,
которая на вход принимает сообщение и пишет его в файл
(имя файла можно задать переменной в начале программы)
"""
import csv
from typing import Optional

from flask import Flask
from werkzeug.exceptions import InternalServerError

app = Flask(__name__)


@app.route("/bank_api/<branch>/<int:person_id>")
def bank_api(branch: str, person_id: int):
    branch_card_file_name = f"bank_data/{branch}.csv"

    with open(branch_card_file_name, "r") as fi:
        csv_reader = csv.DictReader(fi, delimiter=",")

        for record in csv_reader:
            if int(record["id"]) == person_id:
                return record["name"]
        else:
            return "Person not found", 404


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
def handle_exception(e: InternalServerError):
    original: Optional[Exception] = getattr(e, "original_exception", None)

    if isinstance(original, FileNotFoundError):
        write_message(f"Tried to access {original.filename}. Exception info: {original.strerror}\n")
    elif isinstance(original, OSError):
        write_message(f"Unable to access a card. Exception info: {original.strerror}\n")

    return "Internal server error", 500


if __name__ == "__main__":
    app.run()
