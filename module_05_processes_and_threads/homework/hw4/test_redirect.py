import unittest
from unittest import TestCase
from redirect import Redirect
from typing import IO
import traceback
import sys


class TestRedirect(TestCase):
    """Класс с модульными тестами для Redirect"""
    def test_streams_actually_redirected(self):
        """Проверка того, что потоки данных действительно перенаправляются"""
        old_stdout: IO = sys.stdout
        old_stderr: IO = sys.stderr
        new_stdout: IO = open('stdout.txt', 'w')
        new_stderr: IO = open('stderr.txt', 'w')

        with Redirect(stdout=new_stdout, stderr=new_stderr):
            # Если сделать assertEqual внутри блока, то тест не падает. Внутри блока даже self.fail() не падает
            inner_stdout = sys.stdout
            inner_stderr = sys.stderr

        self.assertEqual(new_stdout, inner_stdout)
        self.assertEqual(new_stderr, inner_stderr)
        self.assertNotEqual(old_stdout, inner_stdout)
        self.assertNotEqual(old_stderr, inner_stderr)

    def test_redirected_only_stdout(self):
        """Проверка перенаправления только stdout"""
        text: str = 'Hello, world!'
        new_stdout: IO = open('stdout.txt', 'w')

        try:
            with Redirect(stdout=new_stdout):
                print(text, end='')

            with open('stdout.txt', 'r') as file:
                self.assertEqual(text, file.read())
        except:
            self.fail()

    def test_redirected_only_stderr(self):
        """Проверка перенаправления только stderr"""
        text: str = 'Hello, world!'
        new_stderr: IO = open('stderr.txt', 'w')

        with Redirect(stderr=new_stderr):
            raise ValueError(text)
        with open('stderr.txt', 'r') as file:
            self.assertIn(f'ValueError: {text}', file.read())

    def test_redirecting_without_parameters(self):
        """Проверка работы к/м без параметров"""
        try:
            with Redirect():
                raise ValueError()
        except:
            self.fail()


if __name__ == '__main__':
    with open('test_results.txt', 'a') as test_file_stream:
        runner = unittest.TextTestRunner(stream=test_file_stream)
        unittest.main(testRunner=runner)
