import contextlib
from flask import Flask
from app import free_port
import time


@contextlib.contextmanager
def open_flask_on_free_port(port: int = 5000) -> Flask:
    """
    Контекстный менеджер, открывающий Flask сервер на выбранном порту. Если порт занят, то км освобождает его.
    При выходе порт снова освобождается
    :param port: порт
    :return: Flask приложение
    """
    try:
        free_port(port)
        time.sleep(1)
        yield Flask(__name__)
    finally:
        free_port(port)


if __name__ == '__main__':
    with open_flask_on_free_port(5000) as app:
        app.run(port=5000)
