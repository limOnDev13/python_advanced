"""
Перепишите банковский endpoint, заменив запись сообщений в файл на логирование.
Проверьте работу endpoint-а. Код этого задания мы будем использовать в следующем уроке,
поэтому обязательно выполните его перед изучением следующей темы
"""

import csv
from typing import Optional
import logging

from flask import Flask
from werkzeug.exceptions import InternalServerError


app = Flask(__name__)
logger = logging.getLogger('Bank_api_logger')


@app.route("/bank_api/<branch>/<int:person_id>")
def bank_api(branch: str, person_id: int):
    branch_card_file_name = f"bank_data/{branch}.csv"

    with open(branch_card_file_name, "r", encoding='utf-8') as fi:
        csv_reader = csv.DictReader(fi, delimiter=",")

        for record in csv_reader:
            if int(record["id"]) == person_id:
                return record["name"]
        else:
            logger.warning(f"Person not found.\ndata file: {branch_card_file_name}\nperson_id: {person_id}")
            return "Person not found", 404


@app.errorhandler(FileNotFoundError)
def handle_file_not_found_error(exc: FileNotFoundError):
    logger.exception(f"Tried to access {exc.filename}.", exc_info=exc)
    return "Internal server error", 500


@app.errorhandler(InternalServerError)
def handle_exception(e: InternalServerError):
    logger.debug('Поймали какую-то ошибку!')
    original: Optional[Exception] = getattr(e, "original_exception", None)

    if isinstance(original, OSError):
        logger.exception(f"Unable to access a card.", exc_info=original)
    else:
        logger.exception("Unexpected exception", exc_info=original)
    return "Internal server error", 500


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info('Program was started...')
    app.run()
