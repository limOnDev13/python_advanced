from unittest import TestCase
from fixed_person import Person
from freezegun import freeze_time


class TestPerson(TestCase):
    def setUp(self):
        self.persons: list[Person] = [
            Person('Vova', 1999, 'abc'),
            Person('Sasha', 1),
            Person('Ivan', 2024)
        ]

    @freeze_time('01.01.2024')
    def test_get_age(self):
        """Проверка геттера возраста человека"""
        for person in self.persons:
            with self.subTest(msg=f'year of birth is {person.yob}'):
                correct_answer: int = 2024 - person.yob
                answer: int = person.get_age()

                self.assertEqual(correct_answer, answer)

    def test_get_name(self):
        """Проверка геттера имени"""
        for person in self.persons:
            with self.subTest(msg=f'name is {person.name}'):
                correct_answer: str = person.name
                answer: str = person.get_name()

                self.assertEqual(answer, correct_answer)

    def test_set_name(self):
        """Проверка сеттера имени"""
        names: list[str] = ['a', 'aaa', 'Ivan']
        for new_name, person in zip(names, self.persons):
            with self.subTest(msg=f'new name is {new_name}'):
                person.set_name(new_name)

                self.assertEqual(new_name, person.get_name())

    def test_get_address(self):
        """Проверка геттера адреса"""
        for person in self.persons:
            with self.subTest(msg=f'address is {person.address}'):
                answer: str = person.get_address()
                correct_answer: str = person.address

                self.assertEqual(answer, correct_answer)

    def test_set_address(self):
        """Проверка сеттера адреса"""
        addresses: list[str] = ['', 'aaa', 'bbb']
        for new_address, person in zip(addresses, self.persons):
            with self.subTest(msg=f'new address is {new_address}'):
                person.set_address(new_address)

                self.assertEqual(person.get_address(), new_address)

    def test_is_homeless(self):
        """Проверка метода is_homeless. Если адрес - пустая строка, метод возвращает False"""
        for person in self.persons:
            with self.subTest(msg=f'address is "{person.get_address()}"'):
                self.assertEqual(person.is_homeless(), person.address != '')
