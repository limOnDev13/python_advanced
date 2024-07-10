import sqlite3
import csv


def delete_wrong_fees(
        cursor: sqlite3.Cursor,
        wrong_fees_file: str
) -> None:
    with open(wrong_fees_file, 'r', newline='') as file:
        delete_query: str = """
        DELETE FROM table_fees
        WHERE truck_number = ? AND timestamp = ?
        """
        reader = csv.reader(file)

        cursor.executemany(delete_query, list(reader)[1:])


if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        delete_wrong_fees(cursor, "../wrong_fees.csv")
        conn.commit()
