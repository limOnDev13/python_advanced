import sqlite3


def number_hurricane_days(cursor: sqlite3.Cursor) -> int:
    select_query: str = """
    SELECT COUNT(*) FROM table_kotlin WHERE wind >= 33
    """
    cursor.execute(select_query)

    number_days, *_ = cursor.fetchone()

    return number_days


if __name__ == "__main__":
    with sqlite3.connect('practise.db') as conn:
        print(f'Кол-во ураганных дней: {number_hurricane_days(conn.cursor())}')
