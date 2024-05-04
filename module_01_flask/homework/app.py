import datetime
from flask import Flask
import random
import os
import re

app = Flask(__name__)

list_cars = ['Chevrolet', 'Renault', 'Ford', 'Lada']
list_cats: list[str] = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']


@app.route('/hello_world')
def hello_world() -> str:
    return 'Привет, мир!'


@app.route('/cars')
def cars() -> str:
    global list_cars
    return ', '.join(list_cars)


@app.route('/cats')
def cats() -> str:
    global list_cats
    return random.choice(list_cats)


@app.route('/get_time/now')
def get_time_now():
    return 'Точное время: {}'.format(datetime.datetime.now())


@app.route('/get_time/future')
def get_time_future():
    return 'Точное время через час будет {}'.format(
        datetime.datetime.now() + datetime.timedelta(hours=1)
    )


@app.route('/get_random_word')
def get_random_word():
    return get_word_from_book()


def get_word_from_book() -> str:
    """
    Функция возвращает случайное слово из книги Война и мир. По заданию функционал выведен в отдельную функцию
    :return: Случайное слово (без знаков препинания)
    :rtype: str
    """
    if not hasattr(get_word_from_book, '__words'):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        book_file = os.path.join(base_dir, 'war_and_peace.txt')

        with open(book_file, 'r', encoding='utf-8') as book:
            get_word_from_book.__words = re.findall(r'\b\w+', book.read())

    return random.choice(get_word_from_book.__words)


@app.route('/counter')
def counter():
    counter.__count = counter.__count + 1 if hasattr(counter, '__count') else 1

    return str(counter.__count)


if __name__ == '__main__':
    app.run(debug=True)
