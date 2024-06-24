"""
Представим, что мы работаем в IT отделе крупной компании.
У HR отдела появилась гениальная идея - поздравлять сотрудников
в день рождения однодневным отгулом.

Для этого HR отделу надо предоставить данные на всех
сотрудников вместе с их датами рождения.
Сотрудники у нас работают либо в IT-, либо в PROD-отделе.
Идентификационным номером сотрудника является число,
анкеты сотрудников в формате json вы можете найти в папке fixtures.
В написанное приложение добавьте логи так,
чтобы они помогли найти ошибки со следующими сотрудниками
    отдел IT, сотрудники 1, 2, 3, 4, 5
    отдел PROD, сотрудники 1, 2, 3, 4, 5
"""

import json
from json.decoder import JSONDecodeError
import logging
import os
from datetime import datetime

from flask import Flask

app = Flask(__name__)

logger = logging.getLogger("account_book")

current_dir = os.path.dirname(os.path.abspath(__file__))
fixtures_dir = os.path.join(current_dir, "fixtures")

departments = {"IT": "it_dept", "PROD": "production_dept"}


@app.route("/account/<department>/<int:account_number>/")
def account(department: str, account_number: int):
    dept_directory_name = departments.get(department)

    if dept_directory_name is None:
        return "Department not found", 404

    full_department_path = os.path.join(fixtures_dir, dept_directory_name)

    account_data_file = os.path.join(full_department_path, f"{account_number}.json")

    try:
        with open(account_data_file, "r", encoding='utf-8') as fi:
            account_data_txt = fi.read()
    except FileNotFoundError:
        logger.error(f'Account number not found: {account_number}')
        return f'Account number not found: {account_number}', 400

    try:
        account_data_json = json.loads(account_data_txt)

        name, birth_date = account_data_json["name"], account_data_json["birth_date"]
        if name == '':
            logger.error('field "name" can not be empty!')
            return 'field "name" can not be empty!', 400
        if birth_date == '':
            logger.error('field "birth_date" can not be empty!')
            return 'field "birth_date" can not be empty!', 400

        day, month, year = birth_date.split(".")
        birth_datetime: datetime = datetime(int(year), int(month), int(day))
        if birth_datetime >= datetime.now():
            logger.error(f'Birth date can not be more than today date! birth_date = {birth_date}')
            return f'Birth date can not be more than today date! birth_date = {birth_date}', 400
    except JSONDecodeError:
        logger.error(f'Not able decode json: {account_data_file}')
        return f'Not able decode json: {account_data_file}', 400
    except ValueError:
        logger.error(f'Invalid birth date: {birth_date}')
        return f'Invalid birth date: {birth_date}', 400
    except KeyError:
        logger.error('Invalid form:\nRequired json: {}\nActual json: {}'.format(
            {'name': '...', 'birth_date': '...'}, account_data_json))
        return 'Invalid form:<br>Required json: {}<br>Actual json: {}'.format(
            {'name': '...', 'birth_date': '...'}, account_data_json), 400

    return f"{name} was born on {day}.{month}"


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Started account server")
    app.run(debug=True)
