import unittest

from social_age import get_social_status


class TestSocialAge(unittest.TestCase):
    def test_can_get_child_age(self):
        age = 8
        expected_res = 'ребенок'
        function_res = get_social_status(age)
        self.assertEqual(expected_res, function_res)

    def test_can_get_teenager_age(self):
        """
        Юнит-тест, проверка возраста подростка (от 13 до 18)
        :return: None
        """
        age: int = 15
        expected_res: str = 'подросток'
        function_res: str = get_social_status(age)
        self.assertEqual(expected_res, function_res)

    def test_can_get_adult_age(self):
        """
        Юнит-тест, проверка возраста взрослого (от 18 до 50)
        :return: None
        """
        age: int = 25
        expected_res: str = 'взрослый'
        function_res: str = get_social_status(age)
        self.assertEqual(expected_res, function_res)

    def test_can_get_elderly_age(self):
        """
        Юнит-тест, проверка возраста пожилого (от 50 до 65)
        :return: None
        """
        age: int = 60
        expected_res: str = 'пожилой'
        function_res: str = get_social_status(age)
        self.assertEqual(expected_res, function_res)

    def test_can_get_retiree_age(self):
        """
        Юнит-тест, проверка возраста пенсионера (от 65)
        :return: None
        """
        age: int = 80
        expected_res: str = 'пенсионер'
        function_res: str = get_social_status(age)
        self.assertEqual(expected_res, function_res)

    def test_cannot_pass_str_as_age(self):
        age = 'old'
        with self.assertRaises(ValueError):
            get_social_status(age)

    def test_cannot_negative_num_as_age(self):
        age = -10
        with self.assertRaises(ValueError):
            get_social_status(age)

    def test_cannot_work_with_not_int_and_float(self):
        age = [10]
        with self.assertRaises(ValueError):
            get_social_status(age)
