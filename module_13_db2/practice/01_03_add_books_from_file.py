import sqlite3


def add_books_from_file(c: sqlite3.Cursor, file_name: str) -> None:
    with open(file_name, 'r', encoding='utf-8') as file:
        lines: list[str] = file.read().split('\n')

        for line in lines[1:-1]:
            c.execute("""
            INSERT INTO table_books (ISBN, book_name, author, publish_year) VALUES (?, ?, ?, ?)
            """, line.split(','))


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        add_books_from_file(cursor, "book_list.csv")
        conn.commit()
