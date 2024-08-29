from flask import request
from flask_wtf import FlaskForm
from wtforms import Field, StringField, SelectField

from module_27_postgres_migrations.hw import app, session
from models import User





@app.route('/users', methods=['POST'])
def add_user():
    """""Эндпоинт для добавления нового пользователя"""
    new_user = request.get_json()

    try:
        user_model = User(name=new_user['name'],
                          has_sale=new_user['has_sale'],
                          address=new_user['address'])
    return '', 200


if __name__ == '__main__':
    app.run(debug=True)
