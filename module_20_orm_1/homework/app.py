from flask import Flask, request, jsonify, abort
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

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


if __name__ == '__main__':
    create_db()
    app.run(debug=True)
