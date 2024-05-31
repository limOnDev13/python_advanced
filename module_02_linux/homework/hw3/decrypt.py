"""
Вася решил передать Пете шифрограмму.
Поскольку о промышленных шифрах Вася ничего не знает,
он решил зашифровать сообщение следующим образом: он посылает Пете строку.

Каждый символ строки — либо буква, либо пробел, либо точка «.», либо две точки «..».
Если после какой-то буквы стоит точка, значит, мы оставляем букву без изменений
(об одной точке Вася задумался, чтобы усложнить расшифровку). Саму точку при этом надо удалить.
Если после какой-то буквы стоят две точки, то предыдущий символ надо стереть. Обе точки при этом тоже нужно удалить.
Возможна ситуация, когда сообщение после расшифровки будет пустым.
В качестве результата можно вернуть просто пустую строку.

Примеры шифровок-расшифровок:

абра-кадабра. → абра-кадабра
абраа..-кадабра → абра-кадабра
абраа..-.кадабра → абра-кадабра
абра--..кадабра → абра-кадабра
абрау...-кадабра → абра-кадабра (сначала срабатывает правило двух точек, потом правило одной точки)
абра........ → <пустая строка>
абр......a. → a
1..2.3 → 23
. → <пустая строка>
1....................... → <пустая строка>

Помогите Пете написать программу для расшифровки.
Напишите функцию decrypt, которая принимает на вход шифр в виде строки, а возвращает расшифрованное сообщение.

Программа должна работать через конвейер (pipe):

$ echo  ‘абраа..-.кадабра’ | python3 decrypt.py
абра-кадабра

Команда echo выводит текст (в стандартный поток вывода).
"""

import sys
import re
from typing import Callable
import tracemalloc
import time
from typing import Optional


def decrypt(encryption: str) -> str:
    """
    Функция дешифрует строку согласно условиям задачи
    :param encryption: Зашифрованная строка
    :type encryption: str
    :return: Дешифрованная строка
    :rtype: str
    """
    words: list[str] = encryption.split('.')

    # Сначала применяется правило двух точек, потом одной точки
    for num, match in enumerate(re.finditer(r'\.+', encryption)):
        start: int = match.start()
        end: int = match.end()

        words[num] = words[num][: start - (end - start) // 2]

    return ''.join(words)


def decrypt_without_re(encryption: str) -> str:
    """
    Аналог функции decrypt без использования регулярных выражений - для сравнения объема памяти и времени работы
    :param encryption: Зашифрованная строка
    :type encryption: str
    :return: Дешифрованная строка
    :rtype: str
    """
    while '.' in encryption:
        num_dots: int = 0
        end: int

        for num, sym in enumerate(encryption):
            if sym != '.' and num_dots == 0:
                continue
            elif sym == '.':
                num_dots += 1
            else:
                end = num
                break
        else:
            end = len(encryption)

        if end - num_dots - num_dots // 2 > 0:
            encryption = encryption.replace(encryption[end - num_dots - num_dots // 2: end], '')
        else:
            encryption = encryption.replace(encryption[:end], '')
    return encryption


def super_decrypt(encryption: str) -> str:
    """
    Функция дешифрует строку согласно условиям задачи. После тестов оказалось, что decrypt проигрывает практически
    всегда и во всем decrypt_without_re. Эта функция является смесью decrypt и decrypt_without_re
    :param encryption: Зашифрованная строка
    :type encryption: str
    :return: Дешифрованная строка
    :rtype: str
    """
    while '.' in encryption:
        match: Optional[re.Match] = re.search(r'\.+', encryption)
        start: int = match.start()
        end: int = match.end()

        if start > (end - start) // 2:
            encryption = encryption.replace(encryption[start - (end - start) // 2: end], '')
        else:
            encryption = encryption.replace(encryption[: end], '')

    return encryption


def trace_malloc_and_time(functions: list[Callable[[str], str]]) -> None:
    """
    Функция замеряет используемый объем памяти и время работы каждой функции
    :param functions: Список функций
    :type functions: list[Callable[[str], str]]
    :return: None
    """
    temp: int = 100000
    encryption_tests: list[str] = [
        '.' * temp,
        'a' * temp,
        'a.' * temp,
        'aa.' * temp,
        'a..' * temp,
        'aa..' * temp,
        'a...' * temp,
        'aa...' * temp,
        'a....' * temp,
        'a' + '.' * temp,
        'a' * temp + '.'
    ]
    for test in encryption_tests:
        print(f'Входные данные: {test[:10]} ___ {test[-10:]}')
        for func in functions:
            start: float = time.time()
            tracemalloc.start()
            func(test)
            print('Функция {name} - время работы: {work_time}; использованная память: {memory}'.format(
                name=func.__name__,
                work_time=round(time.time() - start, 6),
                memory=tracemalloc.get_tracemalloc_memory()
            ))
            tracemalloc.stop()
        print('-' * 50)


if __name__ == '__main__':
    data: str = sys.stdin.read()
    decryption: str = decrypt(data)
    print(decryption)

    # print(
    #     f"{super_decrypt('абра-кадабра.')} V абра-кадабра = {super_decrypt('абра-кадабра.') == 'абра-кадабра'}")
    # print(
    #     f"{super_decrypt('абраа..-кадабра')} V абра-кадабра = {super_decrypt('абраа..-кадабра') == 'абра-кадабра'}")
    # print(
    #     f"{super_decrypt('абраа..-.кадабра')} V абра-кадабра = {super_decrypt('абраа..-.кадабра') == 'абра-кадабра'}")
    # print(
    #     f"{super_decrypt('абра--..кадабра')} V абра-кадабра = {super_decrypt('абра--..кадабра') == 'абра-кадабра'}")
    # print(
    #     f"{super_decrypt('абрау...-кадабра')} V абра-кадабра = {super_decrypt('абрау...-кадабра') == 'абра-кадабра'}")
    # print(f"{super_decrypt('абра........')} V  = {super_decrypt('абра........') == ''}")
    # print(f"{super_decrypt('абр......a.')} V a = {super_decrypt('абр......a.') == 'a'}")
    # print(f"{super_decrypt('1..2.3')} V 23 = {super_decrypt('1..2.3') == '23'}")
    # print(f"{super_decrypt('.')} V  = {super_decrypt('.') == ''}")
    # print(
    #     f"{super_decrypt('1.......................')} V  = {super_decrypt('1.......................') == ''}")

    trace_malloc_and_time([decrypt, decrypt_without_re, super_decrypt])
    # Согласно малочисленным тестам в среднем (когда количества точек и символов соразмерны) алгоритм decrypt_without_re
    # лучше по времени и по памяти. В крайних случаях (когда количества точек и символов несоразмерны)
    # алгоритм super_decrypt работает быстрее всех. В средних случаях алгоритмы super_decrypt и decrypt_without_re
    # работают примерно одинаково по времени и памяти (decrypt_without_re чуть лучше)
