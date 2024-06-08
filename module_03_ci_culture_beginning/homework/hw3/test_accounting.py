from unittest import TestCase

from module_02_linux.homework.hw7.accounting import app, storage


class TestAccounting(TestCase):
    """Класс с unit тестами для accounting.py"""
    @classmethod
    def setUpClass(cls):
        """Инициализация клиента Flask перед всеми тестами"""
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        cls.app = app.test_client()
        cls.add_url = '/add'
        cls.calculate_url = '/calculate'

    def setUp(self):
        """Добавление начальных данных в бд перед каждым тестом"""
        storage[2024] = {1: 100, 2: 0, 3: 333}
        storage[2000] = {4: 4000, 5: 0}
        self.correct_dict: dict[int, dict[int, int]] = {
            2024: {1: 100, 2: 0, 3: 333},
            2000: {4: 4000, 5: 0}
        }

    def tearDown(self):
        """Очистка бд после каждого теста"""
        storage.clear()
        self.correct_dict.clear()

    def test_addition_expenses_in_new_year(self):
        """
        Проверка добавления расходов на год и месяц, которых еше нет в бд
        """
        money_str: str = '100'
        date_examples: tuple[str, ...] = ('20250101', '20260101', '99991231')
        for date_str in date_examples:
            with self.subTest(msg=f'Проверка даты {date_str}'):
                year: int = int(date_str[:4])
                month: int = int(date_str[4:6])

                self.correct_dict[year] = {month: 100}
                url: str = '/'.join((self.add_url, date_str, money_str))
                self.app.get(url)

                self.assertEqual(storage, self.correct_dict)

    def test_addition_expenses_in_new_month(self):
        """Проверка добавления расходов на дату, где год имеется в бд, месяц - нет"""
        money_str: str = '100'
        date_examples: tuple[str, ...] = ('20240401', '20240501', '20001231')
        for date_str in date_examples:
            with self.subTest(msg=f'Проверка даты {date_str}'):
                year: int = int(date_str[:4])
                month: int = int(date_str[4:6])

                self.correct_dict[year][month] = 100
                url: str = '/'.join((self.add_url, date_str, money_str))
                self.app.get(url)

                self.assertEqual(storage, self.correct_dict)

    def test_adding_expenses_for_year_and_month_from_db(self):
        """Проверка добавления расходов на дату, где год и месяц имеются в бд"""
        money_str: str = '100'
        date_examples: tuple[str, ...] = ('20240101', '20240201', '20000401')
        for date_str in date_examples:
            with self.subTest(msg=f'Проверка даты {date_str}'):
                year: int = int(date_str[:4])
                month: int = int(date_str[4:6])

                self.correct_dict[year][month] += 100
                url: str = '/'.join((self.add_url, date_str, money_str))
                self.app.get(url)

                self.assertEqual(storage, self.correct_dict)

    def test_addition_expenses_on_non_existent_date(self):
        """Проверка попытки добавления расходов на дату в неправильном формате (YYYYMMDD)"""
        date_str: str = '20241313'
        money_str: str = '100'
        url: str = '/'.join((self.add_url, date_str, money_str))

        with self.assertRaises(ValueError):
            self.app.get(url)

    def test_calculate_with_year_from_db(self):
        """Проверка расчета расходов за год. Год имеется в бд"""
        years: tuple[int, ...] = (2000, 2024)

        for year in years:
            with self.subTest(msg=f'Проверка ендпоинта calculate с годом {year}'):
                url: str = '/'.join((self.calculate_url, str(year)))
                response = self.app.get(url)
                response_str: str = response.data.decode()

                correct_result: str = f'Траты за {year} равны {sum(self.correct_dict[year].values())}'

                self.assertEqual(response_str, correct_result)

    def test_calculate_with_year_and_month_from_db(self):
        """Проверка расчета расходов за месяц. Год и месяц имеются в бд"""
        for year in self.correct_dict.keys():
            for month in self.correct_dict[year].keys():
                with self.subTest(msg='Проверка ендпоинта calculate с годом и месяцем'):
                    url: str = '/'.join((self.calculate_url, str(year), str(month)))
                    response = self.app.get(url)
                    response_str: str = response.data.decode()
                    correct_answer: str = f'Траты за {month} месяц {year} года равны {self.correct_dict[year][month]}'

                    self.assertEqual(response_str, correct_answer)

    def test_calculate_with_year_not_from_db(self):
        """Проверка расчета расходов за год. В бд нет выбранного года"""
        years: tuple[int, int, int] = (1000, 5000, 9999)

        for year in years:
            with self.subTest(msg=f'Проверка ендпоинта calculate с годом {year}'):
                url: str = '/'.join((self.calculate_url, str(year)))
                response = self.app.get(url)
                response_str = response.data.decode()
                correct_answer: str = f'Траты за {year} равны 0'

                self.assertEqual(response_str, correct_answer)

    def test_calculate_with_year_from_db_and_month_not_from_db(self):
        """Проверка расчета расходов за месяц. Выбранный год имеется в бд, а месяц - нет"""
        years = self.correct_dict.keys()
        months: tuple[int, ...] = (6, 7, 8)

        for year in years:
            for month in months:
                with self.subTest(msg=f'Проверка ендпоинта calculate с годом {year} и месяцем {month}'):
                    url: str = '/'.join((self.calculate_url, str(year), str(month)))
                    response = self.app.get(url)
                    response_str: str = response.data.decode()
                    correct_answer: str = f'Траты за {month} месяц {year} года равны 0'

                    self.assertEqual(response_str, correct_answer)

    def test_calculate_with_year_and_month_not_from_db(self):
        """Проверка расчета расходов за месяц. Выбранные год и месяц не имеются в бд"""
        years: tuple[int, ...] = (1000, 5555, 9999)
        months: tuple[int, ...] = (1, 2, 3, 4, 5)

        for year in years:
            for month in months:
                with self.subTest(msg=f'Проверка ендпоинта calculate с годом {year} и месяцем {month}'):
                    url: str = '/'.join((self.calculate_url, str(year), str(month)))
                    response = self.app.get(url)
                    response_str: str = response.data.decode()
                    correct_answer: str = f'Траты за {month} месяц {year} года равны 0'

                    self.assertEqual(response_str, correct_answer)
