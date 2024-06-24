"""
Напишите код, который выводит сам себя.
Обратите внимание, что скрипт может быть расположен в любом месте.
"""

result = 0
for n in range(1, 11):
    result += n ** 2


# До сюда код может быть любым (работающим)
import os


if __name__ == '__main__':
    base_dir: str = os.path.dirname(os.path.abspath(__file__))
    file_name: str = 'self_printing.py'

    with open(os.path.join(base_dir, file_name), 'r') as file:
        for line in file:
            print(line, end='')
