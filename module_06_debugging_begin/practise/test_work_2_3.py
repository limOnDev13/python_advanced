import unittest
from unittest import TestCase
from work_2_3 import app


class TestCalculate(TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['DEBUG'] = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        cls.app = app.test_client()
        cls.url: str = '/calculate'

    @classmethod
    def tearDownClass(cls):
        app.config['DEBUG'] = True
        app.config['TESTING'] = False
        app.config['WTF_CSRF_ENABLED'] = True

    def setUp(self):
        self.correct_form: dict = {
            'formula': ''
        }

    def tearDown(self):
        self.correct_form.clear()

    def test_raising_ZeroDivisionError(self):
        """Негативная проверка выбрасывания ZeroDivisionError"""
        zero_division_formula: str = '1 / 0'
        self.correct_form['formula'] = zero_division_formula

        with self.assertRaises(ZeroDivisionError):
            self.app.post(self.url, data=self.correct_form)

    def test_raising_OverflowError(self):
        """Негативная проверка выбрасывания OverflowError"""
        OverflowError_formula: str = '1e100 ** 1e100'
        self.correct_form['formula'] = OverflowError_formula

        with self.assertRaises(OverflowError):
            self.app.post(self.url, data=self.correct_form)


if __name__ == '__main__':
    unittest.main()
