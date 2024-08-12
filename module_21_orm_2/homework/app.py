from flask import Flask, request, jsonify, abort
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
import json
from typing import Optional

from db import create_db, Book, Student, get_book_from_student, get_all_debtors, ReceivingBooks
import db


app = Flask(__name__)


@app.route('/books', methods=['GET'])
def get_all_books():
    """Получение списка книг в библиотеке"""
    books: list[Book] = Book.get_all_books()
    return jsonify(books_list=[book.to_json() for book in books]), 200


@app.route('/debtors', methods=['GET'])
def get_debtors():
    """Функция - эндпоинт. Возвращает список должников (студентов, которые держат книгу дольше 2 недель)"""
    debtors: list[Student] = get_all_debtors()
    return jsonify(debtors_list=[debtor.to_json() for debtor in debtors]), 200


@app.route('/give_book', methods=['POST'])
def give_book_to_student():
    """Функция - эндпоинт. Выдает книгу студенту (добавляет запись в таблицу receiving_books)"""
    book_id = request.form.get('book_id', type=int)
    student_id = request.form.get('student_id', type=int)
    if book_id is None or student_id is None:
        return 'Invalid input', 400

    try:
        db.give_book_to_student(book_id=book_id, student_id=student_id)
    except NoResultFound:
        abort(404)
    except MultipleResultsFound:
        return 'Ошибка бд: Дублируется student_id или book_id', 500
    except ValueError:
        return 'Такой книги в библиотеке не осталось', 400
    return 'Книга выдана!', 201


@app.route('/get_book_by_title/<string:title>', methods=['GET'])
def get_book_by_title(title: str):
    """Функция - эндпоинт. Выдает книгу по названию"""
    books: list[Book] = Book.get_book_by_title(title)
    return jsonify(books_with_title=[book.to_json() for book in books])


@app.route('/hand_over_book', methods=['POST'])
def hand_over_book_to_library():
    """Функция - эндпоинт. Позволяет сдать книгу в библиотеку
     (удалить соответствующую запись из таблицы receiving_books и изменить записи в др таблицах)"""
    book_id = request.form.get('book_id', type=int)
    student_id = request.form.get('student_id', type=int)
    if book_id is None or student_id is None:
        return 'Invalid input', 400

    try:
        get_book_from_student(book_id, student_id)
    except NoResultFound:
        return 'Записи о долге нет', 404
    return 'Книга успешно сдана', 200


# Ендпоинт для проверки таблицы receiving_books
@app.route('/all_records', methods=['GET'])
def get_all_records():
    records: list = ReceivingBooks.get_all_records()
    return jsonify(records=[record.to_json() for record in records])


@app.route('/count_books_by_author_id/<int:author_id>', methods=['GET'])
def get_count_books_by_authors(author_id: int):
    """Эндпоинт для получения количества книг в библиотеке по id автора"""
    result_dict: dict = {
        'author_id': author_id,
        'count_books': db.get_count_books_by_author_id(author_id)
    }
    return json.dumps(result_dict), 200


@app.route('/get_books_that_student_has_not_read_yet/<int:student_id>', methods=['GET'])
def get_books_that_student_has_not_read_yet(student_id: int):
    """Эндпоинт для получения списка книг каждого автора, которые студент еще не читал,
     но при этом брал другие книги этого автора"""
    books: list[Book] = db.get_books_that_student_has_not_read_yet(student_id)
    return jsonify(books_not_read=[book.to_json() for book in books]), 200


@app.route('/get_avg_count_books', methods=['GET'])
def get_avg_count_books():
    """Эндпоинт для получения среднего количества книг, которые брали студенты в текущем месяце"""
    avg_count_books: Optional[float] = round(db.get_avg_count_books_in_cur_month(), 2)
    if avg_count_books is None:
        return json.dumps({'avg_count_books_in_current_month': 0})
    return json.dumps({'avg_count_books_in_current_month': avg_count_books})


@app.route('/get_most_popular_book', methods=['GET'])
def get_most_popular_book():
    """Функция возвращает самую популярную книгу у студентов, чей средний бал выше 4.0"""
    most_popular_book = db.get_most_popular_book()
    print('most_popular_book =', most_popular_book)
    return jsonify(most_popular_book=most_popular_book.to_json())


if __name__ == '__main__':
    create_db()
    app.run(debug=True)
