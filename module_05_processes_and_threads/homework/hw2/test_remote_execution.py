import unittest
from unittest import TestCase
from remote_execution import app
import datetime


class TestRemoteExecution(TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        cls.app = app.test_client()
        cls.url: str = '/run_code'

    @classmethod
    def tearDownClass(cls):
        app.config['TESTING'] = False
        app.config['DEBUG'] = True
        app.config['WTF_CSRF_ENABLED'] = True

    def setUp(self):
        self.code_examples: dict[str, str] = {
            "print('Hello, world!')": 'Hello, world!\n',
            "def func() -> list[str]:\n"
            "   return [1, 2, 3, 4, 5]": '',  # код ничего не выводит в stdout
            "def func() -> list[str]:\n"
            "   return [1, 2, 3, 4, 5]\n"
            "print(func())": '[1, 2, 3, 4, 5]\n',
            "import datetime\n"
            "print(datetime.datetime.now().day)": f'{datetime.datetime.now().day}\n'
        }
        self.correct_form: dict[str, str | int] = {
            'code': '',
            'timeout': 0
        }

    def tearDown(self):
        self.correct_form.clear()

    def test_input_correct_code_with_large_timeout(self):
        """Проверка ввода корректного python кода, который отработает намного быстрее, чем timeout"""
        timeout: int = 100

        for code, correct_return in self.code_examples.items():
            self.correct_form['code'] = code
            self.correct_form['timeout'] = timeout

            with self.subTest(code=code, timeout=timeout):
                response = self.app.post(self.url, data=self.correct_form)
                response_str: str = response.data.decode()
                self.assertEqual(correct_return, response_str)

    def test_input_correct_code_with_short_timeout(self):
        """Проверка ввода корректного python кода, который отработает дольше, чем timeout"""
        self.correct_form['code'] = "import time\ntime.sleep(10)"
        self.correct_form['timeout'] = 1

        response = self.app.post(self.url, data=self.correct_form)
        response_str: str = response.data.decode()
        self.assertEqual('Исполнение кода не уложилось в данное время', response_str)

    def test_input_incorrect_form(self):
        """Проверка ввода некорректной формы"""
        self.correct_form['asasda'] = 1323123
        self.correct_form.pop('code')
        self.correct_form.pop('timeout')

        response = self.app.post(self.url, data=self.correct_form)
        self.assertEqual(499, response.status_code)

    def test_input_unsafe_code_with_other_commands(self):
        """Проверка ввода что-то еще помимо python кода"""
        self.correct_form['code'] = 'print()"; echo "hacked'
        self.correct_form['timeout'] = 100

        response = self.app.post(self.url, data=self.correct_form)
        self.assertEqual('\n', response.data.decode())

    def test_input_unsafe_code_with_creating_new_processes(self):
        """Негативная проверка ввода кода, который создает новые процессы"""
        self.correct_form['code'] = "from subprocess import run\nrun(['./kill_the_system.sh'])"
        self.correct_form['timeout'] = 100

        self.app.post(self.url, data=self.correct_form)
        self.assertRaises(BlockingIOError)


if __name__ == '__main__':
    unittest.main()
