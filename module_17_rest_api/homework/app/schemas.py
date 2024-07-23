from marshmallow import Schema, fields, validates, validates_schema, ValidationError, post_load

from models import get_book_by_title, Book, get_author_by_name, Author


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str()

    @validates_schema
    def validate_full_name(self, data, **kwargs) -> None:
        """Проверка наличия полного имени в бд"""
        if get_author_by_name(
                data['first_name'], data['last_name'],
                data['middle_name'] if 'middle_name' in data else None):
            raise ValidationError(f"The author with the name {data['first_name']} {data['last_name']}"
                                  f" is already in the database!")

    @post_load
    def create_author(self, data: dict, **kwargs) -> Author:
        return Author(**data)


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Nested(AuthorSchema(), only=('first_name', 'last_name', 'middle_name'))

    @validates('title')
    def validate_title(self, title: str) -> None:
        if get_book_by_title(title) is not None:
            raise ValidationError(
                'Book with title "{title}" already exists, '
                'please use a different title.'.format(title=title)
            )

    @post_load
    def create_book(self, data: dict, **kwargs) -> tuple[Book, Author]:
        author = data.pop('author')
        data['author_id'] = author['id']
        return Book(**data), author
