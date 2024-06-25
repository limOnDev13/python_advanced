"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""
from typing import Dict, Callable
import subprocess
import json
import itertools
import string


LOG_FILE_NAME: str = 'skillbox_json_messages.log'
LOGS: list[dict] = list()


def read_logs(filename: str = LOG_FILE_NAME) -> None:
    """
    Функция считывает файл с логами, десиарилизует их и сохраняет в списке LOGS
    :param filename: Имя файла с логами
    :type filename: str
    :return: None
    """
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            LOGS.append(json.loads(line))


def task1() -> Dict[str, int]:
    """
    1. Сколько было сообщений каждого уровня за сутки.
    @return: словарь вида {уровень: количество}
    """
    levels: set = {'ERROR', 'DEBUG', 'WARNING', 'CRITICAL', 'INFO', 'EXCEPTION'}
    result_dict: dict[str, int] = dict()

    for level in levels:
        command: list[str] = ['grep', '-c', '-F', f'"level": "{level}"', 'skillbox_json_messages.log']
        proc = subprocess.run(command, capture_output=True)
        result_dict[level] = int(proc.stdout)

    return result_dict


def task2() -> int:
    """
    2. В какой час было больше всего логов.
    @return: час
    """
    # Соберем ключевую функцию для группировки логов по часам
    key_func: Callable = lambda line_json: int(line_json['time'][:2])

    # Сгруппируем логи с помощью itertools.groupby и ключевой функции
    # Логи уже отсортированы по времени, поэтому сортировать список не нужно
    max_num_logs: int = 0
    hour_with_max_num_logs: int = 0
    for hour, logs in itertools.groupby(LOGS, key=key_func):
        num_logs: int = len(list(logs))

        if num_logs > max_num_logs:
            hour_with_max_num_logs = hour
            max_num_logs = num_logs

    return hour_with_max_num_logs


def task3() -> int:
    """
    3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
    @return: количество логов
    """
    command: list[str] = ['grep', '-c',
                          '-e', r'"time": "05:[01][0-9]:[0-9][0-9]", "level": "CRITICAL"',
                          '-e', r'"time": "05:20:00", "level": "CRITICAL"',
                          'skillbox_json_messages.log']
    proc = subprocess.run(command, capture_output=True)

    return int(proc.stdout)


def task4() -> int:
    """
    4. Сколько сообщений содержат слово dog.
    @return: количество сообщений
    """
    command: list[str] = ['grep', '-c',
                          r'"message": ".*dog.*',
                          'skillbox_json_messages.log']
    proc = subprocess.run(command, capture_output=True)

    return int(proc.stdout)


def check_punctuation(word: str) -> str:
    """
    Функция убирает знаки препинания с краев у слова и возвращает его
    :param word: Слово
    :type word: str
    :return: слово без знаков препинания
    :rtype: str
    """
    if word[0] in string.punctuation:
        word = word.lstrip()
    if word[-1] in string.punctuation:
        word = word.rstrip()

    return word


def task5() -> tuple[str, int]:
    """
    5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
    @return: слово и количество
    """
    # Получим список всех сообщений в логах WARNING
    warning_logs_messages: list[str] = [log['message'] for log in LOGS if log['level'] == 'WARNING']

    # Соберем список всех слов из каждого сообщения. Слова очистим от знаков препинания и не будем учитывать регистр
    words: list[str] = list()
    for message in warning_logs_messages:
        words.extend([check_punctuation(word.lower()) for word in message.split()])

    # Отсортируем список слов и сгруппируем слова с помощью itertools
    words.sort()
    max_num_words: int = 0
    most_common_word: str = ''
    for word, iter_equal_words in itertools.groupby(words):
        num_words: int = len(list(iter_equal_words))
        if num_words > max_num_words:
            max_num_words = num_words
            most_common_word = word

    return most_common_word, max_num_words


if __name__ == '__main__':
    read_logs()

    tasks = (task1, task2, task3, task4, task5)
    for i, task_fun in enumerate(tasks, 1):
        task_answer = task_fun()
        print(f'{i}. {task_answer}')
