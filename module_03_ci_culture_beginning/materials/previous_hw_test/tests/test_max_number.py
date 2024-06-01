import unittest

from module_03_ci_culture_beginning.materials.previous_hw_test.max_number_app import app


class TestMaxNumberApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/max_number/'

    def test_can_get_correct_max_number_in_series_of_two(self):
        numbers = 1, 2
        url = self.base_url + '/'.join(str(i) for i in numbers)
        response = self.app.get(url)
        response_text = response.data.decode()
        correct_answer_str = f'<i>{max(numbers)}</i>'
        self.assertTrue(correct_answer_str in response_text)

    def test_cannot_get_not_numbers(self):
        """Негативный юнит-тест. Проверяет, что эндпоинт не способен обрабатывать что-то, что не является числом"""
        not_numbers = 'user', 'name'
        url = self.base_url + '/'.join(not_numbers)
        response = self.app.get(url)
        response_text = response.data.decode()
        correct_answer_str = "Переданы некорректные значения"
        self.assertEqual(response_text, correct_answer_str)
