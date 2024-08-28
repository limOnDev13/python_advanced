from flask import request

from module_27_postgres_migrations.hw import app


@app.route('/users', methods=['POST'])
def add_user():
    """""Эндпоинт для добавления нового пользователя"""
    form_data = request.get_json()
    print(form_data)
    return '', 200


if __name__ == '__main__':
    app.run(debug=True)
