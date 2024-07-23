from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import (
    DATA_BOOKS,
    DATA_AUTHORS,
    get_all_books,
    init_db,
    add_book,
    get_book_by_id
)
from schemas import BookSchema

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
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 404

        book = add_book(book)
        return schema.dump(book), 201


class OneBook(Resource):
    def put(self):
        pass

    def get(self, id: int) -> tuple[dict, int]:
        schema = BookSchema()
        return schema.dump(get_book_by_id(id)), 200

    def delete(self):
        pass


api.add_resource(BookList, '/api/books')
api.add_resource(OneBook, '/api/books/<int:id>')

if __name__ == '__main__':
    init_db(initial_records_books=DATA_BOOKS, initial_records_authors=DATA_AUTHORS)
    app.run(debug=True)
