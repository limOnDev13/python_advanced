import datetime
from flask import Flask

app = Flask(__name__)


@app.route('/test')
def test_function():
    now = datetime.datetime.now().utcnow()
    return f'Это тестовая страничка, ответ сгенерирован в {now}'


@app.route('/hello/world')
def hello_world():
    return f'Hello, world!'


@app.route('/counter')
def counter():
    counter.__count = counter.__count + 1 if hasattr(counter, '__count') else 1
    return f'Данная страница открывалась {counter.__count} раз'
