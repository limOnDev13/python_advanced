"""Модуль для сохранения ошибок в отдельный файл.
Пытался сделать через конвейер, но почему-то не считывался стандартный ввод
(команда python -m unittest -v | python3 save_errors.py не работает как надо).
Пришлось сделать через отдельные файлы test_person.txt (тесты файла person.py) и
test_fixed_person.txt (тесты файла fixed_person.py)
"""
import sys


if __name__ == '__main__':
    with open('ERRORS.MD', 'w', encoding='utf-8') as errors_file:
        result_text: str = ('# Исправление ошибок в файле python.py  \n'
                            '## Файл до исправления  \n')
        with open('person.py', 'r', encoding='utf-8') as init_file:
            for line in init_file:
                result_text += ' ' * 4 + line + ' ' * 2

        result_text += '## Результаты unit тестов  \n'
        with open('test_person.txt', 'r', encoding='utf-8') as person_errors:
            for line in person_errors:
                result_text += ' ' * 4 + line + ' ' * 2

        result_text += '## Исправленный файл (называется fixed_person.py)  \n'
        with open('fixed_person.py', 'r', encoding='utf-8') as fixed_file:
            for line in fixed_file:
                result_text += ' ' * 4 + line + ' ' * 2

        result_text += '## Результаты unit тестов  \n'
        with open('test_fixed_person.txt', 'r', encoding='utf-8') as fixed_person_errors:
            for line in fixed_person_errors:
                result_text += ' ' * 4 + line + ' ' * 2

        errors_file.write(result_text)
