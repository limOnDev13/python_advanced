"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""

import sys


def get_mean_size(ls_output: str) -> float:
    """
    Функция принимает результат выполнения команды ls -l и возвращает средний размер файла в каталоге.
    Функция смотрит только файлы в каталоге (без папок) и НЕ обходит внутренние каталоги рекурсивно
    :param ls_output: результат выполнения команды ls -l
    :type ls_output: str
    :raise IOError: Если функция не смогла узнать размер файла
    :return: средний размер файла в каталоге в удобочитаемом формате
    :rtype: float
    """
    lines: list[str] = ls_output[:-1].split('\n')[1:]
    total_memory: int = 0
    num_files: int = 0

    # У каталогов в первой строке первый символ - d. По этому признаку функция будет отличать директории от файлов.
    # 4 столбец - объем файла
    for line in lines:
        if line.startswith('d'):
            continue

        file_info: list[str] = line.split()
        if len(file_info) < 5:
            raise IOError(f'Нет возможности узнать размер файла. Информация о файле:\n{line}')
        total_memory += int(file_info[4])
        num_files += 1

    return round(total_memory / num_files, 3) if len(lines) > 0 else 0


if __name__ == '__main__':
    data: str = sys.stdin.read()
    mean_size: float = get_mean_size(data)
    print(mean_size)
