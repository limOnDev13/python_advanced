import sqlite3


ENABLE_FOREIGN_KEY: str = "PRAGMA foreign_key = ON;"

CREATE_TABLE_DIRECTOR: str = """
CREATE TABLE IF NOT EXISTS director (
    dir_id INTEGER PRIMARY KEY,
    dir_first_name VARCHAR(50),
    dir_last_name VARCHAR(50)
);
"""

CREATE_TABLE_MOVIE: str = """
CREATE TABLE IF NOT EXISTS movie (
    mov_id INTEGER PRIMARY KEY,
    mov_title VARCHAR(50)
);
"""

CREATE_TABLE_ACTORS: str = """
CREATE TABLE IF NOT EXISTS actors (
    act_id INTEGER PRIMARY KEY,
    act_first_name VARCHAR(50),
    act_last_name VARCHAR(50),
    act_gender VARCHAR(1)
);
"""

CREATE_TABLE_MOVIE_DIRECTION: str = """
CREATE TABLE IF NOT EXISTS movie_direction (
    dir_id INTEGER REFERENCES director (dir_id) ON DELETE CASCADE,
    mov_id INTEGER REFERENCES movie (mov_id) ON DELETE CASCADE
);
"""

CREATE_TABLE_OSCAR_AWARDED: str = """
CREATE TABLE IF NOT EXISTS oscar_awarded (
    award_id INTEGER PRIMARY KEY,
    mov_id INTEGER REFERENCES movie (mov_title) ON DELETE CASCADE
);
"""

CREATE_TABLE_MOVIE_CAST: str = """
CREATE TABLE IF NOT EXISTS movie_cast (
    act_id INTEGER REFERENCES actors (act_id) ON DELETE CASCADE,
    mov_id INTEGER REFERENCES movie (mov_id) ON DELETE CASCADE,
    role VARCHAR(50)
)
"""


def create_tables() -> None:
    """Функция создает все таблицы"""
    with sqlite3.connect('task_1.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.executescript(CREATE_TABLE_DIRECTOR)
        cursor.executescript(CREATE_TABLE_MOVIE)
        cursor.executescript(CREATE_TABLE_ACTORS)
        cursor.executescript(CREATE_TABLE_MOVIE_DIRECTION)
        cursor.executescript(CREATE_TABLE_OSCAR_AWARDED)
        cursor.executescript(CREATE_TABLE_MOVIE_CAST)
        cursor.executescript(ENABLE_FOREIGN_KEY)


if __name__ == '__main__':
    create_tables()
