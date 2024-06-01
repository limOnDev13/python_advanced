import unittest

from module_03_ci_culture_beginning.materials.previous_hw_test.hello_word_with_day import app


class TestMaxNumberApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    def test_can_get_greetings_with_name(self):
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue(username in response_text)

    def stest_cannot_work_with_some_strings_in_url(self):
        username: str = 'user/name'
        with self.assertRaises(FileNotFoundError):
            response = self.app.get(self.base_url + username)

