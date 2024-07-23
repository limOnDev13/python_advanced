import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

DATA_BOOKS = [
    {'id': 0, 'title': 'Капитанская дочка', 'author': 1},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 3},
    {'id': 3, 'title': 'Бородино', 'author': 2},
]
DATA_AUTHORS: list[dict] = [
    {'id': 0, 'first_name': 'Александр', 'last_name': 'Пушкин', 'middle_name': 'Сергеевич'},
    {'id': 1, 'first_name': 'Михаил', 'last_name': 'Лермонтов', 'middle_name': 'Юрьевич'},
    {'id': 2, 'first_name': 'Герман', 'last_name': 'Мелвилл', 'middle_name': None},
]

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME: str = 'authors'


@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    id: Optional[int] = None

    def __getitem__(self, item: str) -> int | str:
        return getattr(self, item)


@dataclass
class Book:
    title: str
    author_id: int
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


def init_db(initial_records_books: List[Dict],
            initial_records_authors: list[dict]) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{BOOKS_TABLE_NAME}';
            """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript(
                f"""
                PRAGMA foreign_key = ON;
                
                CREATE TABLE IF NOT EXISTS `{AUTHORS_TABLE_NAME}` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    middle_name TEXT
                );
                """
            )
            cursor.executescript(
                f"""
                CREATE TABLE IF NOT EXISTS `{BOOKS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT,
                    author_id INTEGER REFERENCES {AUTHORS_TABLE_NAME} (id) ON DELETE CASCADE
                );
                """
            )
            cursor.executemany(
                f"""
                INSERT INTO `{AUTHORS_TABLE_NAME}`
                (first_name, last_name, middle_name) VALUES (?, ?, ?)
                """,
                [
                    (item['first_name'], item['last_name'], item['middle_name'])
                    for item in initial_records_authors
                ]
            )
            cursor.executemany(
                f"""
                INSERT INTO `{BOOKS_TABLE_NAME}`
                (title, author_id) VALUES (?, ?)
                """,
                [
                    (item['title'], item['author'])
                    for item in initial_records_books
                ]
            )


def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id=row[0], title=row[1], author_id=row[2])


def _get_author_obj_from_row(row: tuple) -> Author:
    return Author(
        id=row[0], first_name=row[1], last_name=row[2],
        middle_name=row[3] if len(row) == 4 else None)


def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}`')
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` 
            (title, author_id) VALUES (?, ?)
            """,
            (book.title, book.author_id)
        )
        book.id = cursor.lastrowid
        return book


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE id = ?
            """,
            (book_id,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def update_book_by_id(book: Book) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {BOOKS_TABLE_NAME}
            SET title = ?, author = ?
            WHERE id = ?
            """,
            (book.title, book.author_id, book.id)
        )
        conn.commit()


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE id = ?
            """,
            (book_id,)
        )
        conn.commit()


def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE title = ?
            """,
            (book_title,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def get_author_by_name(first_name: str, last_name: str, middle_name: Optional[str] = None) -> Optional[Author]:
    """Получение автора по полному имени"""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM {AUTHORS_TABLE_NAME}
            WHERE first_name = ? AND last_name = ? AND middle_name = ? 
            """, (first_name, last_name, middle_name)
        )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)
