import sqlite3


def drop_table_with_birds() -> None:
    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()
        drop_query: str = """
        DROP TABLE IF EXISTS table_birds
        """
        cursor.execute(drop_query)
        conn.commit()


def create_table_with_birds() -> None:
    """Не нашел таблицы с птицами, поэтому функция создаст ее"""
    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()
        create_query: str = """
        CREATE TABLE IF NOT EXISTS table_birds
        (
        id INTEGER,
        bird_name TEXT,
        date_time TEXT
        )
        """
        cursor.execute(create_query)
        conn.commit()


if __name__ == "__main__":
    drop_table_with_birds()
    create_table_with_birds()  # Создадим таблицу, если ее не существует
