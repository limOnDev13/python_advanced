import sqlite3
import dataclasses


def add_10_records_to_table_warehouse(cursor: sqlite3.Cursor) -> None:
    names: str = 'asdfghjklz'
    descriptions: str = 'qwertyuiop'
    amount: range = range(10)

    for name, description, number in zip(names, descriptions, amount):
        cursor.execute("""
        INSERT INTO table_warehouse (name, description, amount) VALUES (?, ?, ?)
        """, (name, description, number))


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        add_10_records_to_table_warehouse(cursor)
        conn.commit()
