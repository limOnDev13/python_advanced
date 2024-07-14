from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
from typing import List

from models import init_db, get_all_books, DATA
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


@app.route('/books')
def all_books() -> str:
    return render_template(
        'index.html',
        books=get_all_books(),
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


if __name__ == '__main__':
    init_db(DATA)
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
