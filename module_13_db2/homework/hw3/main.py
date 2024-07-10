import datetime
import sqlite3


# def drop_table_with_birds() -> None:
#     with sqlite3.connect('../homework.db') as conn:
#         cursor = conn.cursor()
#         drop_query: str = """
#         DROP TABLE IF EXISTS table_birds
#         """
#         cursor.execute(drop_query)
#         conn.commit()
#
#
# def create_table_with_birds() -> None:
#     """Не нашел таблицы с птицами, поэтому функция создаст ее"""
#     with sqlite3.connect('../homework.db') as conn:
#         cursor = conn.cursor()
#         create_query: str = """
#         CREATE TABLE IF NOT EXISTS table_birds
#         (
#         id INTEGER PRIMARY KEY,
#         bird_name TEXT,
#         date_time TEXT
#         )
#         """
#         cursor.execute(create_query)
#         conn.commit()


def log_bird(
        cursor: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
) -> None:
    insert_query: str = """
    INSERT INTO table_birds (bird_name, date_time) VALUES (?, ?)
    """
    cursor.execute(insert_query, (bird_name, date_time))


def check_if_such_bird_already_seen(
        cursor: sqlite3.Cursor,
        bird_name: str
) -> bool:
    select_query: str = """
    SELECT EXISTS(SELECT bird_name WHERE COUNT(bird_name) > 1 and bird_name = ?)
    """
    cursor.execute(select_query, (bird_name,))
    result, *_ = cursor.fetchone()
    return result


if __name__ == "__main__":
    print("Программа помощи ЮНатам v0.1")
    name: str = input("Пожалуйста введите имя птицы\n> ")
    count_str: str = input("Сколько птиц вы увидели?\n> ")
    count: int = int(count_str)
    right_now: str = datetime.datetime.utcnow().isoformat()

    # drop_table_with_birds()
    # create_table_with_birds()  # Создадим таблицу, если ее не существует

    with sqlite3.connect("../homework.db") as connection:
        cursor: sqlite3.Cursor = connection.cursor()

        log_bird(cursor, name, right_now)

        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")
