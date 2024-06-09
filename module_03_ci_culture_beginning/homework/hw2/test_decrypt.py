from unittest import TestCase

from module_03_ci_culture_beginning.homework.hw2.decrypt import decrypt


class TestDecrypt(TestCase):
    def check_examples(self, examples: list[tuple[str, str]]) -> None:
        """
        Метод прогоняет переданный список примеров через тестируемую функцию. Код вынесен в отдельную функцию,
        чтобы не дублировать его
        :param examples: Список примеров. Примеры имеют вид кортежей, первый элемент - шифровка, второй - дешифровка
        :return: None
        """
        for example in examples:
            with self.subTest(msg='Неправильная дешифровка!',
                              encryption=example[0], wrong_decryption=decrypt(example[0]), rigth_decryption=example[1]):
                self.assertEqual(decrypt(example[0]), example[1])

    def test_encryption_with_one_dot(self):
        """Проверка шифровки с одной точкой"""
        examples: list[tuple[str, str]] = [
            ('абра-кадабра.', 'абра-кадабра'),
            ('.', '')
        ]

        self.check_examples(examples)

    def test_encryption_with_two_dots(self):
        """Проверка шифровки с двумя точками подряд"""
        examples: list[tuple[str, str]] = [
            ('абраа..-кадабра', 'абра-кадабра'),
            ('абра--..кадабра', 'абра-кадабра')
        ]

        self.check_examples(examples)

    def test_encryption_with_more_two_dots_but_less_number_of_characters(self):
        """Проверка шифровки с 3 и более точками подряд, но менее, чем количество символов перед ними"""
        examples: list[tuple[str, str]] = [
            ('абрау...-кадабра', 'абра-кадабра'),
        ]

        self.check_examples(examples)

    def test_encryption_with_dots_more_than_characters(self):
        """Проверка шифровки, когда половина количества подряд идущих точек больше,
        чем количество символов перед ними"""
        examples: list[tuple[str, str]] = [
            ('абра........', ''),
            ('абр......a.', 'a'),
            ('1.......................', '')
        ]

        self.check_examples(examples)

    def test_other_encryption(self):
        """Проверка шифровок, которые не попали в предыдущие категории"""
        examples: list[tuple[str, str]] = [
            ('абраа..-.кадабра', 'абра-кадабра'),
            ('1..2.3', '23')
        ]

        self.check_examples(examples)

