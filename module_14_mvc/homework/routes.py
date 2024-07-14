from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
from typing import List, Optional

from models import get_all_books, DATA
import models

app: Flask = Flask(__name__)


class NewBookForm(FlaskForm):
    book_title = StringField(validators=[InputRequired()])
    author_name = StringField(validators=[InputRequired()])


def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
<table>
    <thead>
    <tr>
        <th>ID</td>
        <th>Title</td>
        <th>Author</td>
    </tr>
    </thead>
    <tbody>
        {books_rows}
    </tbody>
</table>
"""
    rows: str = ''
    for book in books:
        rows += '<tr><td>{id}</tb><td>{title}</tb><td>{author}</tb></tr>'.format(
            id=book['id'], title=book['title'], author=book['author'],
        )
    return table.format(books_rows=rows)


@app.route('/books', methods=['GET'])
def all_books() -> str:
    """Функция - эндпоинт. Показывает таблицу книг. Если указать автора в GET-запросе (по ключ. слову 'author'),
    то покажет таблицу книг этого автора в бд"""
    author: Optional[str] = request.args.get('author', type=str, default=None)
    if author is None:
        return render_template(
            'index.html',
            books=get_all_books(),
        )
    return render_template(
        'index.html',
        books=models.get_author_books(author)
    )


@app.route('/books/form', methods=['GET', 'POST'])
def get_books_form() -> tuple[str, int]:
    if request.method == 'GET':
        return render_template('add_book.html'), 200
    else:
        form = NewBookForm()

        if form.validate_on_submit():
            title, author = form.book_title.data, form.author_name.data
            models.add_new_book(title, author)
            return 'Книга добавлена в базу данных!<br><a href="http://localhost:5000/books">Список всех книг</a>', 200
        return f'Неправильно заполненная форма! {form.errors}', 400


@app.route('/books/<int:book_id>')
def get_book_with_id(book_id: int) -> tuple[str, int]:
    return render_template(
        'index.html',
        books=models.get_book_with_id(book_id)
    ), 200


if __name__ == '__main__':
    models.update_table_books(DATA)
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
