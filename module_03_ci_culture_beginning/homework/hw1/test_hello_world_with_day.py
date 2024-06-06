from unittest import TestCase
from freezegun import freeze_time

from module_03_ci_culture_beginning.homework.hw1.hello_word_with_day import app


class TestHelloWorldWithDay(TestCase):
    """Класс с unit тестами для hello_world_with_day.py"""
    @classmethod
    def setUpClass(cls):
        """Инициализация клиента Flask"""
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        cls.app = app.test_client()
        cls.base_url = '/hello-world/'

    @freeze_time('2024-06-03')
    def test_correctness_receiving_today_monday(self):
        """Проверка корректности определения понедельника"""
        username: str = 'username'
        url: str = self.base_url + username
        response = self.app.get(url)
        response_text: str = response.data.decode()
        correct_answer: str = f'Привет, {username}. Хорошего понедельника!'
        self.assertEqual(response_text, correct_answer)

    @freeze_time('2024-06-04')
    def test_correctness_receiving_today_tuesday(self):
        """Проверка корректности определения вторника"""
        username: str = 'username'
        url: str = self.base_url + username
        response = self.app.get(url)
        response_text: str = response.data.decode()
        correct_answer: str = f'Привет, {username}. Хорошего вторника!'
        self.assertEqual(response_text, correct_answer)

    @freeze_time('2024-06-05')
    def test_correctness_receiving_today_wednesday(self):
        """Проверка корректности определения среды"""
        username: str = 'username'
        url: str = self.base_url + username
        response = self.app.get(url)
        response_text: str = response.data.decode()
        correct_answer: str = f'Привет, {username}. Хорошей среды!'
        self.assertEqual(response_text, correct_answer)

    @freeze_time('2024-06-06')
    def test_correctness_receiving_today_thursday(self):
        """Проверка корректности определения четверга"""
        username: str = 'username'
        url: str = self.base_url + username
        response = self.app.get(url)
        response_text: str = response.data.decode()
        correct_answer: str = f'Привет, {username}. Хорошего четверга!'
        self.assertEqual(response_text, correct_answer)

    @freeze_time('2024-06-07')
    def test_correctness_receiving_today_friday(self):
        """Проверка корректности определения пятницы"""
        username: str = 'username'
        url: str = self.base_url + username
        response = self.app.get(url)
        response_text: str = response.data.decode()
        correct_answer: str = f'Привет, {username}. Хорошей пятницы!'
        self.assertEqual(response_text, correct_answer)

    @freeze_time('2024-06-08')
    def test_correctness_receiving_today_saturday(self):
        """Проверка корректности определения субботы"""
        username: str = 'username'
        url: str = self.base_url + username
        response = self.app.get(url)
        response_text: str = response.data.decode()
        correct_answer: str = f'Привет, {username}. Хорошей субботы!'
        self.assertEqual(response_text, correct_answer)

    @freeze_time('2024-06-09')
    def test_correctness_receiving_today_sunday(self):
        """Проверка корректности определения воскресенья"""
        username: str = 'username'
        url: str = self.base_url + username
        response = self.app.get(url)
        response_text: str = response.data.decode()
        correct_answer: str = f'Привет, {username}. Хорошего воскресенья!'
        self.assertEqual(response_text, correct_answer)

    def test_username_is_greetings(self):
        """Проверка ответа на ввод пожелания хорошего дня в username"""
        username: str = 'ХорОшей СРЕды'
        url: str = self.base_url + username
        response = self.app.get(url)
        response_text: str = response.data.decode()
        correct_answer: str = 'Спасибо! И вам того же)'
        self.assertEqual(response_text, correct_answer)
