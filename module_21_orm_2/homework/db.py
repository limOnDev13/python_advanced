from sqlalchemy import (create_engine, Column, Integer, Text, Date, Float,
                        Boolean, DateTime, and_, or_, ForeignKey, func, select, desc)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.exc import NoResultFound
from sqlalchemy.event import listens_for
from datetime import datetime
from typing import Optional
import csv
import random
import string
import re


engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'), nullable=False)
    author = relationship('Author', back_populates='books')

    student_book_associations = relationship('ReceivingBooks', back_populates='books')

    def __repr__(self) -> str:
        return (f'id: {self.id} | title: {self.name} | count:  {self.count} | '
                f'release_date: {self.release_date} | author_id: {self.author_id}')

    def to_json(self) -> dict:
        """Метод собирает поля объекта в словарь"""
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    @classmethod
    def get_all_books(cls) -> list:
        """Метод возвращает список всех книг"""
        return session.query(Book).all()

    @classmethod
    def get_book_by_id(cls, book_id: int) -> Optional['Book']:
        """Функция выдает книгу по id, если такая имеется"""
        return session.query(Book).filter(Book.id == book_id).one_or_none()

    @classmethod
    def get_book_by_title(cls, title: str) -> list:
        """Метод возвращает список книг, у которых в названии есть title"""
        return session.query(Book).filter(Book.name.like(f'%{title}%')).all()


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    books = relationship('Book', back_populates='author', cascade='all, delete, delete-orphan', lazy='joined')

    def __repr__(self) -> str:
        return f'id: {self.id} | name: {self.name} | surname:  {self.surname}'


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    student_book_associations = relationship(
        'ReceivingBooks', back_populates='student', cascade='all, delete, delete-orphan'
    )
    books = association_proxy('student_book_associations', 'book')

    def __repr__(self) -> str:
        return (f'id: {self.id} | name: {self.name} | surname:  {self.surname} | '
                f'phone: {self.phone} | email: {self.email}'
                f'average_score: {self.average_score} | scholarship: {self.scholarship}')

    def to_json(self) -> dict:
        """Метод собирает поля объекта в словарь"""
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    @classmethod
    def get_all_students_with_scholarship(cls) -> list:
        """Метод возвращает список студентов со стипендией. В задании написано с общежитием,
         но в предложенной таблице нет такого поля"""
        return session.query(Student).filter(Student.scholarship).all()

    @classmethod
    def get_all_students_with_score_more(cls, score: float) -> list:
        """Метод возвращает список студентов с баллом выше, чем score"""
        return session.query(Student).filter(Student.average_score > score).all()


class ReceivingBooks(Base):
    __tablename__ = 'receiving_book'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'))
    student_id = Column(Integer, ForeignKey('student.id'))
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime, default=None)

    student = relationship('Student', back_populates='student_book_associations')
    books = relationship('Book', back_populates='student_book_associations', lazy='joined')

    def __repr__(self) -> str:
        return (f'id: {self.id} | book_id: {self.book_id} | student_id:  {self.student_id} | '
                f'date_of_issue: {self.date_of_issue} | author_id: {self.date_of_return}')

    @hybrid_property
    def count_date_with_books(self):
        if self.date_of_return is None:
            return None
        return self.date_of_return - self.date_of_issue


    @classmethod
    def get_all_records(cls):
        return session.query(ReceivingBooks).all()

    def to_json(self) -> dict:
        """Метод собирает поля объекта в словарь"""
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


def get_book_from_student(book_id: int, student_id: int):
    """Метод получает от студента книгу. Если нет связки book_id - student_id - выбросит ошибку"""
    # Установим дату возврата книги на сегодня
    receiving_book = session.query(ReceivingBooks).filter(and_(
        ReceivingBooks.student_id == student_id,
        ReceivingBooks.book_id == book_id,
        ReceivingBooks.date_of_return.is_(None))
    ).first()
    if receiving_book is None:
        raise NoResultFound()
    receiving_book.date_of_return = datetime.today()

    # Увеличим количество данной книги в библиотеке на 1
    book = Book.get_book_by_id(book_id)
    book.count += 1

    session.commit()


def give_book_to_student(book_id: int, student_id: int) -> None:
    """Метод выдает книгу студенту (если книга и студент есть в бд и количество книг в библиотеке не равно 0
     - т.е. что не все книги раздали)"""
    # Проверим, что книга и студент имеются в бд
    book: Book = session.query(Book).filter(Book.id == book_id).first()
    session.query(Student).filter(Student.id == student_id).first()

    # Проверим, что количество данной книге больше 0
    if book.count <= 0:
        raise ValueError('Такая книга закончилась в библиотеке')
    else:
        # Раз книгу выдаем, то и ее количество в библиотеке уменьшается на 1
        book.count -= 1

    # Добавим запись о выдаче книги
    new_receiving_book = ReceivingBooks(book_id=book_id, student_id=student_id, date_of_issue=datetime.today())
    session.add(new_receiving_book)

    session.commit()


def get_all_debtors(term: int = 14) -> list:
    """Метод возвращает список должников (которые держат книгу дольше, чем term)"""
    return session.query(Student).filter(and_(
        Student.id == ReceivingBooks.student_id,
        or_(ReceivingBooks.count_date_with_books.is_(None), ReceivingBooks.count_date_with_books > term))
    ).all()


def get_count_books_by_author_id(author_id: int) -> int:
    """Функция возвращает количество книг в библиотеке по id автора"""
    return session.query(func.sum(Book.count)).filter_by(author_id=author_id).scalar()


def get_books_that_student_has_not_read_yet(student_id: int) -> list:
    """Функция возвращает список книг каждого автора, которые студент еще не читал,
     но при этом брал другие книги этого автора"""
    # Получим таблицу с id книги и id автора, которые прочитал студент с student_id
    books_read_q = session.query(ReceivingBooks.book_id.label('rec_book_id'), Author.id.label('rec_author_id')) \
        .join(ReceivingBooks.books).join(Book.author) \
        .filter(ReceivingBooks.student_id.__eq__(student_id)).subquery()

    # Вернем только те книги, id которых нет в books_read_query, но id автора есть в books_read_query
    return session.query(Book).filter(and_(
        Book.id.not_in(select(books_read_q.c.rec_book_id)),
        Book.author_id.in_(select(books_read_q.c.rec_author_id)))).all()


def get_avg_count_books_in_cur_month() -> float:
    """Функция возвращает среднее количество книг, которые студенты брали в течение текущего месяца"""
    # Получим таблицу с student_id и количеством книг, взятых в этом месяце
    nums_books_q = session.query(ReceivingBooks.student_id, func.count(ReceivingBooks.book_id).label('count_books')) \
        .filter(and_(
            func.extract('year', ReceivingBooks.date_of_issue) == datetime.today().year,
            func.extract('month', ReceivingBooks.date_of_issue) == datetime.today().month)) \
        .group_by(ReceivingBooks.student_id)
    # Вернем среднее количество
    return session.query(func.avg(nums_books_q.subquery().c.count_books)).scalar()


def get_most_popular_book():
    """Функция возвращает самую популярную книгу у студентов, чей балл выше 4.0"""
    # Получим таблицу id книг и количества студентов, которые брали эту книгу, и у которых средний бал выше 4.0
    books_of_best_students_q = session.query(
        ReceivingBooks.book_id.label('best_book_id'), func.count(ReceivingBooks.student_id).label('count_books')) \
        .join(Student.student_book_associations) \
        .filter(Student.average_score > 4.0) \
        .group_by(ReceivingBooks.book_id).subquery()
    return session.query(Book).join(books_of_best_students_q, Book.id == books_of_best_students_q.c.best_book_id)\
        .order_by(desc(books_of_best_students_q.c.count_books)) \
        .limit(1).one()


def get_top_most_reading_students() -> list:
    """Функция возвращает ТОП-10 самых читающих студентов в этом году"""
    # Получим таблицу студентов и количества взятых ими книг в этом году
    reading_students_q = session.query(
        ReceivingBooks.student_id.label('read_student_id'), func.count(ReceivingBooks.book_id).label('count_books')) \
        .filter(func.extract('year', ReceivingBooks.date_of_issue) == datetime.today().year) \
        .group_by(ReceivingBooks.student_id).subquery()
    return session.query(Student).join(reading_students_q, Student.id == reading_students_q.c.read_student_id) \
        .order_by(desc(reading_students_q.c.count_books)) \
        .limit(10).all()


def load_students_from_csv(csv_file: str) -> bool:
    """Функция считывает информацию о студентах из csv файла и добавляет ее в бд"""
    with open(csv_file, 'r', encoding='utf-8') as file:
        file_reader = csv.DictReader(
            file, delimiter=';',
            fieldnames=['name', 'surname', 'phone', 'email', 'average_score', 'scholarship'])

        rows: list[dict] = list(file_reader)
        for row in rows:
            row['scholarship'] = bool(row['scholarship'])

        with session.begin():
            session.bulk_insert_mappings(Student, rows)
            return True


def create_csv_with_students_data(num_students: int = 100, csv_file: str = 'students_data.csv') -> None:
    """Функция создает файл csv со случайными студентами"""
    with open(csv_file, 'w', encoding='utf-8') as file:
        for _ in range(num_students):
            name: str = ''.join((random.choice(string.ascii_lowercase) for _ in range(random.randint(2, 10))))
            surname: str = ''.join((random.choice(string.ascii_lowercase) for _ in range(random.randint(2, 10))))
            phone: str = ''.join((random.choice(string.ascii_lowercase) for _ in range(10)))
            email: str = ''.join((random.choice(string.ascii_lowercase) for _ in range(10)))
            average_score: float = random.uniform(0, 10)
            scholarship: bool = random.choice((0, 1))

            file.write(';'.join((name, surname, phone, email, str(average_score), str(scholarship))) + '\n')


@listens_for(Student.phone, 'set')
def validate_student_phone(target, value, oldvalue, initiator):
    """Функция - валидатор номера телефона студента"""
    if not re.match(r'\+7\(9\d{2}\)-\d{3}-\d{2}-\d{2}$', value):
        raise ValueError('Student phone must have format +7(9**)-***-**-**')


def create_db() -> None:
    """Функция создает бд"""
    Base.metadata.create_all(engine)

    check_books_exists = session.query(Book).all()
    check_students_exists = session.query(Student).all()
    check_author_exists = session.query(Author).all()

    if not check_books_exists:
        session.add(Book(
            name='test_title1', count=3, release_date=datetime.strptime('01-01-2000', '%d-%M-%Y'),
            author_id=1
        ))
        session.add(Book(
            name='test_title2', count=3, release_date=datetime.strptime('01-01-2000', '%d-%M-%Y'),
            author_id=1
        ))
        session.add(Book(
            name='test_title3', count=3, release_date=datetime.strptime('01-01-2000', '%d-%M-%Y'),
            author_id=2
        ))
    if not check_author_exists:
        session.add(Author(name='test_author_name_1', surname='test_author_surname_1'))
        session.add(Author(name='test_author_name_2', surname='test_author_surname_2'))
    if not check_students_exists:
        session.add(Student(
            name='test_name', surname='test_surname',
            phone='test_phone', email='test_email',
            average_score=5.5, scholarship=True))
        session.add(Student(
            name='test_name2', surname='test_surname2',
            phone='test_phone2', email='test_email2',
            average_score=1.1, scholarship=False))
    session.commit()


if __name__ == '__main__':
    create_csv_with_students_data()
    create_db()
