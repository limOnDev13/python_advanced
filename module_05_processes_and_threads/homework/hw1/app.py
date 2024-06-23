"""
Консольная утилита lsof (List Open Files) выводит информацию о том, какие файлы используют какие-либо процессы.
Эта команда может рассказать много интересного, так как в Unix-подобных системах всё является файлом.

Но нам пока нужна лишь одна из её возможностей.
Запуск lsof -i :port выдаст список процессов, занимающих введённый порт.
Например, lsof -i :5000.

Как мы с вами выяснили, наш сервер отказывается запускаться, если кто-то занял его порт. Напишите функцию,
которая на вход принимает порт и запускает по нему сервер. Если порт будет занят,
она должна найти процесс по этому порту, завершить его и попытаться запустить сервер ещё раз.
"""
from typing import List
import subprocess
from subprocess import Popen
import shlex
import time

from flask import Flask

app = Flask(__name__)


def get_pids(port: int) -> List[int]:
    """
    Возвращает список PID процессов, занимающих переданный порт
    @param port: порт
    @return: список PID процессов, занимающих порт
    """
    if not isinstance(port, int):
        raise ValueError

    command_line: str = f'lsof -i :{port}'
    command: list[str] = shlex.split(command_line)
    processes_on_port_info = subprocess.run(command, capture_output=True).stdout.decode()

    # Распарсим результат
    processes_on_port: list[str] = processes_on_port_info.split('\n')[1:-1]

    pids: list[int] = [int(process_info[1]) for process_info in
                       [line.split() for line in processes_on_port]]

    return pids


def free_port(port: int) -> None:
    """
    Завершает процессы, занимающие переданный порт
    @param port: порт
    """
    pids: List[int] = get_pids(port)

    processes: list[Popen] = [Popen(shlex.split(f'kill {pid}')) for pid in pids]

    for proc in processes:
        proc.wait()


def run(port: int) -> None:
    """
    Запускает flask-приложение по переданному порту.
    Если порт занят каким-либо процессом, завершает его.
    @param port: порт
    """
    free_port(port)
    time.sleep(1)
    app.run(port=port)


if __name__ == '__main__':
    run(5000)
