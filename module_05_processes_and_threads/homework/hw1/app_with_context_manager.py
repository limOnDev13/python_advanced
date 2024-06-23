"""Решение первой задачи через контекстный менеджер. Сделано просто так"""
from flask import Flask
import time
from app import free_port


class FreePort:
    """
    Контекстный менеджер для запуска сервера на Flask на свободном порте. Если порт занят другими процессами,
    то они завершаются
    Args:
        port (int) - номер порта
    """
    def __init__(self, port: int = 5000):
        if not isinstance(port, int):
            raise ValueError
        self.port: int = 5000

    def __enter__(self):
        """При заходе в контекстный менеджер выбранный порт освобождается. Возвращает объект Flask"""
        free_port(self.port)
        time.sleep(1)
        return Flask(__name__)

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """При выходе освобождает порт (не придумал, что надо делать)"""
        pass


if __name__ == '__main__':
    port: int = 5000
    with FreePort(port) as app:
        app.run(port=port)
