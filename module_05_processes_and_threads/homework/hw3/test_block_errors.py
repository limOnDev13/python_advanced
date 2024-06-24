import unittest
from unittest import TestCase
from block_errors import BlockErrors


class TestBlockErrors(TestCase):
    """Класс с модульными тестами для BlockErrors"""
    def test_code_without_exception(self):
        """Проверка к/м с блоком кода без ошибок"""
        try:
            with BlockErrors({Exception}):
                a = 1
        except:
            self.fail()

    def test_ignore_exception(self):
        """Проверка игнорирования ошибки"""
        try:
            with BlockErrors({ZeroDivisionError}):
                a = 1 / 0
        except:
            self.fail()

    def test_exception_raises_upper(self):
        """Проверка прокидывания ошибки выше"""
        with self.assertRaises(ZeroDivisionError):
            with BlockErrors({TypeError}):
                a = 1 / 0

    def test_error_check_is_higher_in_inner_block_and_ignoring_in_outer_one(self):
        """Проверка прокидывания ошибки выше во внутреннем блоке и игнорирования во внешнем"""
        try:
            outer_err_types = {TypeError}
            with BlockErrors(outer_err_types):
                inner_err_types = {ZeroDivisionError}
                with BlockErrors(inner_err_types):
                    a = 1 / '0'
        except:
            self.fail()

    def test_for_ignoring_child_errors(self):
        """Проверка игнорирования дочерних ошибок"""
        try:
            err_types = {Exception}
            with BlockErrors(err_types):
                a = 1 / '0'
        except:
            self.fail()


if __name__ == '__main__':
    unittest.main()
