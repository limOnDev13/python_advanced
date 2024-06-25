"""
Заменим сообщение "The requested URL was not found on the server" на что-то более информативное.
Например, выведем список всех доступных страниц с возможностью перехода по ним.

Создайте Flask Error Handler, который при отсутствии запрашиваемой страницы будет выводить
список всех доступных страниц на сайте с возможностью перехода на них.
"""
import functools
from flask import Flask
from typing import Callable, Any
from werkzeug.exceptions import NotFound

app = Flask(__name__)
URLS: list[str] = list()
BASE_URL: str = 'http://localhost:5000'  # Пока не понял, как получить его программно


def save_url(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(url, **kwargs) -> Any:
        URLS.append(f'<a href>{BASE_URL}{url}</a>')  # ссылки подсвечиваются, но почему-то не работают
        return func(url, **kwargs)
    return wrapper


@save_url(app.route)('/dogs')  # Пока не придумал, как нормально декорировать
def dogs():
    return 'Страница с пёсиками'


@save_url(app.route)('/cats')
def cats():
    return 'Страница с котиками'


@save_url(app.route)('/cats/<int:cat_id>')
def cat_page(cat_id: int):
    return f'Страница с котиком {cat_id}'


@save_url(app.route)('/index')
def index():
    return 'Главная страница'


@app.errorhandler(404)
def handle_url_not_found(exc: NotFound):
    return f'Страница не найдена!<br>Доступные ссылки: {URLS}', 404


if __name__ == '__main__':
    print(URLS)
    app.run(debug=True)
