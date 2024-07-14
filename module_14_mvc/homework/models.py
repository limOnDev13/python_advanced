import sqlite3
from typing import Any, Optional, List

DATA: List[dict] = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy'},
]


class Book:

    def __init__(self, id: int, title: str, author: str, number_views: int) -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.number_views: int = number_views

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_books'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `table_books` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, 
                    author TEXT,
                    number_views INTEGER DEFAULT 0
                )
                """
            )
            cursor.executemany(
                """
                INSERT INTO `table_books`
                (title, author) VALUES (?, ?)
                """,
                [
                    (item['title'], item['author'])
                    for item in initial_records
                ]
            )


def delete_table() -> None:
    """Функция удаляет страницу"""
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.executescript(
            """
            DROP TABLE IF EXISTS table_books
            """
        )


def update_table_books(initial_records: list[dict]) -> None:
    """Фнкция удаляет таблицу и создает новую"""
    delete_table()
    init_db(initial_records=initial_records)


def increase_number_views(cursor: sqlite3.Cursor, book_ids: list[int]):
    """Функция увеличивает количество просмотров (number_views) книг по id из списка ids на единицу при каждом вызове.
    """
    for book_id in book_ids:
        book_id = int(book_id)

        # Проверим, что данный id есть в бд
        cursor.execute(
            """
            SELECT EXISTS(SELECT id FROM table_books WHERE id = ?)
            """, (book_id,)
        )
        if cursor.fetchone()[0]:
            cursor.execute(
                """
                UPDATE table_books
                SET number_views = number_views + 1
                WHERE id = ?
                """, (book_id,)
            )


def get_all_books() -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * from `table_books`
            """
        )
        # После получения списка обновим количество просмотров у каждой книги. Так обновление происходит после
        # просмотра, то появляется небольшой рассинхрон - пользователь видит количество просмотров, не учитывая текущий
        # просмотр
        results = cursor.fetchall()
        increase_number_views(cursor, [row[0] for row in results])
        return [Book(*row) for row in results]


def add_new_book(title: str, author: str) -> None:
    """Функция добавляет новую книгу в бд"""
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO table_books (title, author) VALUES (?, ?)
            """, (title, author)
        )
        conn.commit()


def get_author_books(author: str) -> List[Book]:
    """Функция возвращает список книг автора из бд"""
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM table_books WHERE author = ?
            """, (author,)
        )

        # Обновим данные о просмотрах
        results = cursor.fetchall()
        increase_number_views(cursor, [row[0] for row in results])
        return [Book(*row) for row in results]


def get_book_with_id(book_id: int) -> List[Book]:
    """Функция возвращает книгу по индексу. Возвращает ее в формате List[Book], чтобы воспользоваться index.html"""
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM table_books WHERE id = ?
            """, (book_id,)
        )

        result = cursor.fetchone()
        if not result:
            return []
        else:
            increase_number_views(cursor, [book_id])
            return [Book(*result)]
