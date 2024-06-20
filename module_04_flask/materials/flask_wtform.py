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


@app.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        name: str = str(form.name.data)
        if not re.fullmatch(r'[A-Z][a-z]+ [A-Z]\. [A-Z]\.', name):
            return f'Имя должно иметь формат Фамилия И. О. {name} не подходит!', 400

        email: str = str(form.email.data)
        if not re.match(r'[A-Za-z0-9.]+@[A-Za-z]+\.[A-Za-z]+\b', email):
            return f'Некорректный email!', 400

        phone: int = int(form.phone.data)
        if len(str(phone)) != 10:
            return f'Телефон должен быть длиной в 10 символов!', 400

        return f"Successfully registered user {email} with phone +7{phone}"

    return f"Invalid input, {form.errors}", 400


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
