from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, swag_from, Swagger
from apispec.ext.marshmallow import MarshmallowPlugin
from werkzeug.serving import WSGIRequestHandler

from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError
from typing import Optional

from models import (
    DATA_BOOKS, DATA_AUTHORS, get_all_books, init_db, add_book, get_book_by_id,
    Book, delete_book_by_id, update_book_by_id, Author, add_author, get_all_authors,
    get_author_by_id, delete_author_by_id
)
from doc_files.author_docs import authors_list_get, authors_list_post, one_author_get, one_author_delete, swag_json
from schemas import BookSchema, AuthorSchema


BOOK_NOT_FOUND: dict = {'status': 'Book not found!'}
AUTHOR_NOT_FOUND: dict = {'status': 'Author not found!'}

spec = APISpec(
    title='BookList',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)
app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    @swag_from('doc_files\\books_list_get.yml')
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    @swag_from('doc_files\\books_list_post.yml')
    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = BookSchema()
        try:
            book, author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book = add_book(book)
        add_author(author)
        return schema.dump(book), 201


class OneBook(Resource):
    @swag_from('doc_files\\one_book_put.yml')
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

    @swag_from('doc_files\\one_book_get.yml')
    def get(self, id: int) -> tuple[dict, int]:
        schema = BookSchema()
        book: Optional[Book] = get_book_by_id(id)
        if book:
            return schema.dump(book), 200
        else:
            return BOOK_NOT_FOUND, 404

    @swag_from('doc_files\\one_book_delete.yml')
    def delete(self, id: int) -> tuple[dict, int]:
        schema = BookSchema()
        deleted_book: Optional[Book] = delete_book_by_id(id)
        if deleted_book:
            return schema.dump(deleted_book), 200
        else:
            return BOOK_NOT_FOUND, 404


class AuthorsList(Resource):
    @swag_from(authors_list_get)
    def get(self) -> tuple[dict, int]:
        schema = AuthorSchema()
        return schema.dump(get_all_authors(), many=True), 200

    @swag_from(authors_list_post)
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
    @swag_json("doc_files\\example_flassger.json", api_path='/api/authors/{id}')
    def get(self, id: int) -> tuple[dict, int]:
        schema = AuthorSchema()
        author = get_author_by_id(id)
        if author is None:
            return AUTHOR_NOT_FOUND, 404
        return schema.dump(get_author_by_id(id)), 200

    @swag_json("doc_files\\example_flassger.json", api_path='/api/authors/{id}')
    def delete(self, id: int) -> tuple[dict, int]:
        schema = AuthorSchema()
        deleted_book: Optional[Author] = delete_author_by_id(id)
        if deleted_book is None:
            return AUTHOR_NOT_FOUND, 404
        return schema.dump(deleted_book), 202


template = spec.to_flasgger(
    app,
    definitions=[BookSchema]
)
swagger = Swagger(app, template=template)


api.add_resource(OneAuthor, '/api/authors/<int:id>')
api.add_resource(AuthorsList, '/api/authors')
api.add_resource(BookList, '/api/books')
api.add_resource(OneBook, '/api/books/<int:id>')

if __name__ == '__main__':
    init_db(initial_records_books=DATA_BOOKS, initial_records_authors=DATA_AUTHORS)
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug=True)
