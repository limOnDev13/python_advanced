from unittest import TestCase
from flask_wtform import app
from flask import Response


class TestLuckyTicket(TestCase):
    """Класс с модульными тестами для эндпоинта lucky_ticket"""
    @classmethod
    def setUpClass(cls):
        app.config['DEBUG'] = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        cls.app = app.test_client()
        cls.base_url: str = '/lucky_ticket'

    @classmethod
    def tearDownClass(cls):
        app.config['DEBUG'] = True
        app.config['TESTING'] = False
        app.config['WTF_CSRF_ENABLED'] = True

    def setUp(self):
        self.unlucky_ticket: dict = {
            'name': 'Ivan',
            'family_name': 'Ivanov',
            'ticket_number': '123456'
        }
        self.lucky_ticket: dict = {
            'name': 'Vova',
            'family_name': 'Volosnikov',
            'ticket_number': '123600'
        }

    def tearDown(self):
        self.unlucky_ticket.clear()
        self.lucky_ticket.clear()

    def test_correct_lucky_ticket(self):
        """Проверка ввода корректной формы со счастливым билетом"""
        response: Response = self.app.post(self.base_url, data=self.lucky_ticket)
        response_str: str = response.data.decode()
        correct_answer: str = 'Поздравляем вас, {name} {family_name}'.format(
            name=self.lucky_ticket['name'],
            family_name=self.lucky_ticket['family_name']
        )
        self.assertEqual(correct_answer, response_str)

    def test_correct_unlucky_ticket(self):
        """Проверка ввода корректной формы с несчастливым билетом"""
        response: Response = self.app.post(self.base_url, data=self.unlucky_ticket)
        response_str: str = response.data.decode()
        correct_answer: str = 'Неудача. Попробуйте еще раз!'.format(
            name=self.unlucky_ticket['name'],
            family_name=self.unlucky_ticket['family_name']
        )
        self.assertEqual(correct_answer, response_str)

    def test_input_without_name(self):
        """Негативная проверка ввода формы без имени"""
        self.lucky_ticket.pop('name')
        response: Response = self.app.post(self.base_url, data=self.lucky_ticket)
        response_str: str = response.data.decode()
        correct_answer: str = 'Поле name обязательно для заполнения!'
        self.assertEqual(correct_answer, response_str)

    def test_input_without_family_name(self):
        """Негативная проверка ввода формы без фамилии"""
        self.lucky_ticket.pop('family_name')
        response: Response = self.app.post(self.base_url, data=self.lucky_ticket)
        response_str: str = response.data.decode()
        correct_answer: str = 'Поле family_name обязательно для заполнения!'
        self.assertEqual(correct_answer, response_str)

    def test_input_without_ticket_number(self):
        """Негативная проверка ввода формы без номера билета"""
        self.lucky_ticket.pop('ticket_number')
        response: Response = self.app.post(self.base_url, data=self.lucky_ticket)
        response_str: str = response.data.decode()
        correct_answer: str = 'Поле ticket_number обязательно для заполнения!'
        self.assertEqual(correct_answer, response_str)

    def test_input_ticket_number_start_with_0(self):
        """Негативная проверка ввода номера билета, начинающегося на 0"""
        self.lucky_ticket['ticket_number'] = '012345'
        response: Response = self.app.post(self.base_url, data=self.lucky_ticket)
        response_str: str = response.data.decode()
        correct_answer: str = 'Номер билета не может начинаться с 0!'
        self.assertEqual(correct_answer, response_str)

    def test_input_incorrect_ticket_number(self):
        """Негативная проверка ввода некорректного номера билета"""
        incorrect_numbers: list[str] = ['asdasda', '', '1', '1234567', 'asd123', '123asd']

        for number in incorrect_numbers:
            with self.subTest(incorrect_number=number):
                self.lucky_ticket['ticket_number'] = number
                response: Response = self.app.post(self.base_url, data=self.lucky_ticket)
                response_str: str = response.data.decode()
                correct_answer: str = 'Номер билета должен состоять из 6 цифр!'
                self.assertEqual(correct_answer, response_str)
