from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError
from typing import Optional

from models import (
    DATA_BOOKS, DATA_AUTHORS, get_all_books, init_db, add_book, get_book_by_id,
    Book, delete_book_by_id, update_book_by_id, Author, add_author, get_all_authors,
    get_author_by_id, delete_author_by_id
)
from schemas import BookSchema, AuthorSchema


BOOK_NOT_FOUND: dict = {'status': 'Book not found!'}
AUTHOR_NOT_FOUND: dict = {'status': 'Author not found!'}

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = BookSchema()
        try:
            book, author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 404

        book = add_book(book)
        author = add_author(author)
        return schema.dump(book), 201


class OneBook(Resource):
    def put(self, id: int):
        schema = BookSchema()
        data = request.json
        try:
            new_book_data, new_author_info = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 404

        result: Optional[Book, Author] = update_book_by_id(
            book_id=id, new_book_data=new_book_data, new_author_data=new_author_info)

        if result is None:
            return BOOK_NOT_FOUND, 404
        return schema.dump(result[0]), 202

    def get(self, id: int) -> tuple[dict, int]:
        schema = BookSchema()
        book: Optional[Book] = get_book_by_id(id)
        if book:
            return schema.dump(book), 200
        else:
            return BOOK_NOT_FOUND, 404

    def delete(self, id: int) -> tuple[dict, int]:
        schema = BookSchema()
        deleted_book: Optional[Book] = delete_book_by_id(id)
        if deleted_book:
            return schema.dump(deleted_book), 200
        else:
            return BOOK_NOT_FOUND, 404


class AuthorsList(Resource):
    def get(self) -> tuple[dict, int]:
        schema = AuthorSchema()
        return schema.dump(get_all_authors(), many=True), 200

    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = add_author(author)
        return schema.dump(author), 201


class OneAuthor(Resource):
    def get(self, id: int) -> tuple[dict, int]:
        schema = AuthorSchema()
        return schema.dump(get_author_by_id(id)), 200

    def delete(self, id: int) -> tuple[dict, int]:
        schema = AuthorSchema()
        deleted_book: Optional[Author] = delete_author_by_id(id)
        if deleted_book is None:
            return AUTHOR_NOT_FOUND, 404
        return schema.dump(deleted_book), 202


api.add_resource(OneAuthor, '/api/authors/<int:id>')
api.add_resource(AuthorsList, '/api/authors')
api.add_resource(BookList, '/api/books')
api.add_resource(OneBook, '/api/books/<int:id>')

if __name__ == '__main__':
    init_db(initial_records_books=DATA_BOOKS, initial_records_authors=DATA_AUTHORS)
    app.run(debug=True)
