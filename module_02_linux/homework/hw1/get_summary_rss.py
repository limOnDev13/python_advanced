"""
С помощью команды ps можно посмотреть список запущенных процессов.
С флагами aux эта команда выведет информацию обо всех процессах, запущенных в системе.

Запустите эту команду и сохраните выданный результат в файл:

$ ps aux > output_file.txt

Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""
from typing import Optional


def get_summary_rss(ps_output_file_path: str) -> str:
    """
    Функция считывает информацию о запущенных процессах из файла и возвращает суммарный потребляемый объем памяти
    в человекочитаемом формате
    :param ps_output_file_path: Путь до файла с информацией о запущенных процессах
    :type ps_output_file_path: str
    :return: суммарный потребляемый объем памяти в человекочитаемом формате
    :rtype: str
    """
    # 1) Считаем информацию из файла
    with open(ps_output_file_path, 'r', encoding='utf-8') as output:
        lines: list[str] = output.read()[:-1].split('\n')[1:]

        # 2) Информация о потребляемой памяти находится в столбце RSS ([5] столбец)
        total_memory: int = 0
        for line in lines:
            data: list[str] = line.split()
            total_memory += int(data[5])

        # 3) Вернем результат в человекочитаемом формате
        return f'Общий потребляемый объем памяти: {beautiful_format(total_memory)}'


UNITS: list[str] = ['Б', "Кб", "Мб", "Гб", "Тб"]
LIMITS: list[int] = [0 if degree == 0 else 1024 ** degree for degree in range(5)]


def beautiful_format(num_bytes: int) -> str:
    """
    Функция переводит количество байтов в удобочитаемый формат. Дальше Тб функция не переводит
    :param num_bytes: Количество байтов
    :type num_bytes: int
    :return: Объем в человекочитаемом формате
    :rtype: str
    """
    res_limit: int = 0
    res_unit: Optional[str] = None

    # Переберем все границы объемов, пока не найдем тот, который будет больше переданного количества байтов
    for limit, unit in zip(LIMITS, UNITS):
        if num_bytes < limit:
            return '{volume} {unit}'.format(
                volume=num_bytes if res_unit == 'Б' else round(num_bytes / res_limit, 3),
                unit=res_unit
            )
        elif num_bytes >= limit:
            res_limit = limit
            res_unit = unit

    # Если функция не вернула значение и дошла до этой точки, значит объем больше 1 Тб. Вернем его
    return '{volume} {unit}'.format(
        volume=num_bytes if res_unit == 'Б' else round(num_bytes / res_limit, 3),
        unit=res_unit
    )


if __name__ == '__main__':
    path: str = 'output_file.txt'
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)
