"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""

import unittest
from unittest import TestCase
from hw1_registration import app
from flask import Response


class TestRegistration(TestCase):
    """Класс с юнит тестами для flask_wtform.py"""
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        cls.app = app.test_client()
        cls.base_url: str = '/registration'

    @classmethod
    def tearDownClass(cls):
        app.config['TESTING'] = False
        app.config['DEBUG'] = True
        app.config['WTF_CSRF_ENABLED'] = True

    def setUp(self):
        self.correct_form: dict = {
            'email': 'example@email.com',
            'phone': 9999999999,
            'name': 'Ivanov I. I.',
            'address': 'test address',
            'index': 1,
            'comment': 'test_comment'
        }

    def tearDown(self):
        self.correct_form.clear()

    def test_input_correct_form(self):
        """Проверка ввода корректных значений формы"""
        response: Response = self.app.post(self.base_url, data=self.correct_form)
        response_text: str = response.data.decode()
        correct_answer: str = (f"Successfully registered user {self.correct_form['email']}"
                               f" with phone +7{self.correct_form['phone']}")
        self.assertEqual(response_text, correct_answer)

    def test_input_incorrect_email(self):
        """Негативная проверка ввода некорректного еmail"""
        incorrect_emails: list[str] = ['exampleemail.com', '@email.com', 'example@.com', 'example@emailcom',
                                       'example@email.', 'exampleemailcom', '']

        for email in incorrect_emails:
            self.correct_form['email'] = email

            with self.subTest('Негативный тест на ввод email', email=email):
                response: Response = self.app.post(self.base_url, data=self.correct_form)

                self.assertEqual(response.status_code, 400)

    def test_input_incorrect_phone(self):
        """Негативная проверка ввода некорректного номера телефона"""
        incorrect_phones: list = [1, 11111111111, 'aaaaaaaaaaa', -1111111111]

        for phone in incorrect_phones:
            self.correct_form['phone'] = phone

            with self.subTest('Негативный тест на ввод телефона', phone=phone):
                response: Response = self.app.post(self.base_url, data=self.correct_form)

                self.assertEqual(response.status_code, 400)

    def test_input_form_without_name(self):
        """Негативная проверка ввода формы без имени"""
        self.correct_form.pop('name')
        response: Response = self.app.post(self.base_url, data=self.correct_form)
        correct_answer: str = 'Поле имя обязательно для заполнения!'
        self.assertEqual(400, response.status_code)

    def test_input_form_without_phone(self):
        """Негативная проверка ввода формы без phone"""
        self.correct_form.pop('phone')
        response: Response = self.app.post(self.base_url, data=self.correct_form)
        correct_answer: str = 'Поле phone обязательно для заполнения!'
        self.assertEqual(400, response.status_code)

    def test_input_form_without_email(self):
        """Негативная проверка ввода формы без email"""
        self.correct_form.pop('email')
        response: Response = self.app.post(self.base_url, data=self.correct_form)
        correct_answer: str = 'Поле email обязательно для заполнения!'
        self.assertEqual(400, response.status_code)

    def test_input_form_without_address(self):
        """Негативная проверка ввода формы без address"""
        self.correct_form.pop('address')
        response: Response = self.app.post(self.base_url, data=self.correct_form)
        self.assertEqual(400, response.status_code)

    def test_input_form_without_index(self):
        """Негативная проверка ввода формы без index"""
        self.correct_form.pop('index')
        response: Response = self.app.post(self.base_url, data=self.correct_form)
        self.assertEqual(400, response.status_code)


if __name__ == '__main__':
    unittest.main()
