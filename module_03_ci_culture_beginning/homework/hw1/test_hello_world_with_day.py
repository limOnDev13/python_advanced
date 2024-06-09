from unittest import TestCase
from freezegun import freeze_time
from datetime import datetime, timedelta

from module_03_ci_culture_beginning.homework.hw1.hello_word_with_day import app


class TestHelloWorldWithDay(TestCase):
    """Класс с unit тестами для hello_world_with_day.py"""
    @classmethod
    def setUpClass(cls):
        """Инициализация клиента Flask"""
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        cls.app = app.test_client()
        cls.base_url = '/hello-world/'
        cls.greetings: tuple[str, ...] = (
            'Хорошего понедельника',
            'Хорошего вторника',
            'Хорошей среды',
            'Хорошего четверга',
            'Хорошей пятницы',
            'Хорошей субботы',
            'Хорошего воскресенья'
        )

    @classmethod
    def now_with_offset(cls, offset: int, now: datetime = datetime.now()) -> datetime:
        """
        Метод возвращает день, который наступит через offset дней после now
        :param offset: Количество дней после now
        :type offset: int
        :param now: текущий день
        :type now: datetime
        :return: Дату через offset после now
        :rtype: datetime
        """
        return now + timedelta(days=offset)

    def test_can_get_correct_weekday(self):
        """Проверка получения корректной даты"""
        username: str = 'username'

        for delta_day in range(7):
            date: datetime = self.now_with_offset(delta_day)
            weekday: int = date.weekday()

            with (self.subTest(msg=f'Weekday is {weekday}'), freeze_time(date)):
                url: str = self.base_url + username
                response = self.app.get(url)
                response_text: str = response.data.decode()
                self.assertIn(response_text,
                              (f'Привет, {username}. {greeting}!'
                               for greeting in self.greetings))

    def test_username_is_greetings(self):
        """Проверка ответа на ввод пожелания хорошего дня в username"""
        username: str = 'ХорОшей СРЕды'
        url: str = self.base_url + username
        response = self.app.get(url)
        response_text: str = response.data.decode()
        correct_answer: str = 'Спасибо! И вам того же)'
        self.assertEqual(response_text, correct_answer)
