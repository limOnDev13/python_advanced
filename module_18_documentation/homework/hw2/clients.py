import json
from werkzeug.serving import WSGIRequestHandler
import requests
import logging


logging.basicConfig(level=logging.DEBUG)


class BookClient:
    URL: str = 'http://127.0.0.1:5000/api/books'
    TIMEOUT: int = 5
    book_not_found: str = "Book not found! Response message: {message}"

    def __init__(self):
        self.session = requests.Session()

    def get_all_books(self) -> dict:
        response = self.session.get(self.URL, timeout=self.TIMEOUT)
        return response.json()

    def add_new_book(self, data: dict):
        response = self.session.post(self.URL, json=data, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def get_one_book(self, id: int) -> dict:
        """Метод для получения информации о книге по id. Если книги нет, то выбросится исключение KeyError"""
        response = self.session.get(self.URL + str(id), timeout=self.TIMEOUT)
        if response.status_code == 200:
            return response.json()
        raise KeyError(self.book_not_found.format(response.json()))

    def change_book(self, id: int, data: dict) -> dict:
        """Метод для изменения книги по id. Если книги нет в бд, то выбросится исключение KeyError"""
        response = self.session.put(self.URL + str(id), json=data, timeout=self.TIMEOUT)
        if response.status_code == 202:
            return response.json()
        raise KeyError(self.book_not_found.format(response.json()))

    def delete_book(self, id: int) -> dict:
        """Метод для удаления книги из бд. Если книги нет в бд - выбросится исключение KeyError"""
        response = self.session.delete(self.URL + str(id))
        if response.status_code == 200:
            return response.json()
        raise KeyError(self.book_not_found.format(response.json()))


if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    client = BookClient()
    client.session.post(
        client.URL,
        data=json.dumps({'title': '123', 'author': 'name'}),
        headers={'content-type': 'application/json'}
    )
