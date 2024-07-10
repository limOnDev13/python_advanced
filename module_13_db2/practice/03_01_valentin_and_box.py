import sqlite3
from typing import List

defeated_enemies = [
    "Иванов Э.",
    "Петров Г.",
    "Левченко Л.",
    "Михайлов М.",
    "Яковлев Я",
    "Кузнецов К.",
]


def remove_all_defeated_enemies(
        c: sqlite3.Cursor,
        defeated_enemies: List[str]
) -> None:
    delete_query: str = """
    DELETE FROM table_enemies
    WHERE name = ?
    """
    c.executemany(delete_query, ((enemy, ) for enemy in defeated_enemies))


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        remove_all_defeated_enemies(cursor, defeated_enemies)
        conn.commit()
