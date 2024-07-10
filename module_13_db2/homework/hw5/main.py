import sqlite3
import random
from string import ascii_lowercase


def generate_test_data(
        cursor: sqlite3.Cursor,
        number_of_groups: int
) -> None:
    # 1) Сгенерируем группы
    levels: list[int] = [1, 2, 2, 3]
    for group_num in range(number_of_groups):
        teams: list[tuple] = [
            (''.join(random.choice(ascii_lowercase) for _ in range(3)),  # Имя
             ''.join(random.choice(ascii_lowercase) for _ in range(5)),  # Страна
             level) for level in levels
        ]

        # Добавим команды в таблицу uefa_commands
        insert_into_commands_query: str = """
        INSERT INTO uefa_commands (command_name, command_country, command_level) VALUES (?, ?, ?)
        """
        cursor.executemany(insert_into_commands_query, teams)

        # Добавим команды в таблицу uefa_draw
        insert_into_draw_query: str = """
        INSERT INTO uefa_draw (command_number, group_number)
        VALUES ((SELECT command_number FROM uefa_commands WHERE command_name = ?), ?)
        """
        cursor.executemany(insert_into_draw_query, ((team[0], group_num) for team in teams))


if __name__ == '__main__':
    number_of_groups: int = int(input('Введите количество групп (от 4 до 16): '))
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        generate_test_data(cursor, number_of_groups)
        conn.commit()
