import sqlite3

sql_script_to_execute = """
UPDATE table_russian_post
    SET order_day = replace(order_day, '-05-', '-06-')
    WHERE order_day LIKE '%-05-%'
"""


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        cursor.executescript(sql_script_to_execute)
        conn.commit()
