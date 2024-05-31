"""
Реализуйте endpoint /hello-world/<имя>, который возвращает строку «Привет, <имя>. Хорошей пятницы!».
Вместо хорошей пятницы endpoint должен уметь желать хорошего дня недели в целом, на русском языке.

Пример запроса, сделанного в субботу:

/hello-world/Саша  →  Привет, Саша. Хорошей субботы!
"""

from flask import Flask
from datetime import datetime

app = Flask(__name__)


week: tuple[str, ...] = tuple(['его понедельника', "его вторника", "ей среды", "его четверга",
                               "ей пятницы", "ей субботы", "его воскресенья"])


@app.route('/hello-world/<name>')
def hello_world(name: str):
    return f'Привет, {name}. Хорош{week[datetime.today().weekday()]}!'


if __name__ == '__main__':
    app.run(debug=True)
