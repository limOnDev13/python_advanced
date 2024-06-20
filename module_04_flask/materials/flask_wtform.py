from flask import Flask, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired, NumberRange, Email
from werkzeug.datastructures import ImmutableMultiDict
import re
import json

app = Flask(__name__)


class RegistrationForm(FlaskForm):
    email = StringField()
    phone = IntegerField()
    name = StringField()
    address = StringField()
    index = IntegerField()
    comment = StringField()


class Ticket(FlaskForm):
    name = StringField()
    family_name = StringField()
    ticket_number = StringField()


@app.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        name: str = form.name.data
        if name is None:
            return f'Поле имя обязательно для заполнения!', 400
        if not re.fullmatch(r'[A-Z][a-z]+ [A-Z]\. [A-Z]\.', name):
            return f'Имя должно иметь формат Фамилия И. О. {name} не подходит!', 400

        email: str = form.email.data
        if email is None:
            return f'Поле email обязательно для заполнения!', 400
        if not re.match(r'[A-Za-z0-9.]+@[A-Za-z]+\.[A-Za-z]+\b', email):
            return f'Некорректный email!', 400

        phone: int = form.phone.data
        if phone is None:
            return f'Поле phone обязательно для заполнения!', 400
        if len(str(phone)) != 10:
            return f'Телефон должен быть длиной в 10 символов!', 400

        address: str = form.address.data
        if address is None:
            return f'Поле address обязательно для заполнения!', 400

        return f"Successfully registered user {email} with phone +7{phone}"

    return f"Invalid input, {form.errors}", 400


@app.route('/lucky_ticket', methods=['POST'])
def lucky_ticket() -> tuple[str, int]:
    """Функция - эндпоинт. С помощью POST запроса получает данные о билете и проверяет его, является ли он счастливым"""
    form = Ticket()

    if form.validate_on_submit():
        name: str = form.name.data
        if name is None:
            return 'Поле name обязательно для заполнения!', 400

        family_name: str = form.family_name.data
        if family_name is None:
            return 'Поле family_name обязательно для заполнения!', 400

        number: str = form.ticket_number.data
        if number is None:
            return 'Поле ticket_number обязательно для заполнения!', 400
        if not re.fullmatch(r'\d{6}', number):
            return 'Номер билета должен состоять из 6 цифр!', 400
        if number[0] == '0':
            return 'Номер билета не может начинаться с 0!', 400

        if sum(map(int, number[:3])) == sum(map(int, number[3:])):
            return f'Поздравляем вас, {name} {family_name}', 200
        else:
            return f'Неудача. Попробуйте еще раз!', 200


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
