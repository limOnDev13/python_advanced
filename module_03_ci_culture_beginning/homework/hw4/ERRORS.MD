# Исправление ошибок в файле python.py  
## Файл до исправления  
    
      class Person:
          def __init__(self, name: str, year_of_birth: int, address: str = '') -> None:
              self.name: str = name
              self.yob: int = year_of_birth
              self.address: str = address
      
          def get_age(self) -> int:
              now: datetime.datetime = datetime.datetime.now()
              return self.yob - now.year
      
          def get_name(self) -> str:
              return self.name
      
          def set_name(self, name: str) -> None:
              self.name = self.name
      
          def set_address(self, address: str) -> None:
              self.address == address
      
          def get_address(self) -> str:
              return self.address
      
          def is_homeless(self) -> bool:
              '''
              returns True if address is not set, false in other case
              '''
              return address is None
  ## Результаты unit тестов  
    test_get_address (test_person.TestPerson.test_get_address)
      Проверка геттера адреса ... ok
      test_get_age (test_person.TestPerson.test_get_age)
      Проверка геттера возраста человека ... 
        test_get_age (test_person.TestPerson.test_get_age) [year of birth is 1999]
      Проверка геттера возраста человека ... ERROR
        test_get_age (test_person.TestPerson.test_get_age) [year of birth is 1]
      Проверка геттера возраста человека ... ERROR
        test_get_age (test_person.TestPerson.test_get_age) [year of birth is 2024]
      Проверка геттера возраста человека ... ERROR
      test_get_name (test_person.TestPerson.test_get_name)
      Проверка геттера имени ... ok
      test_is_homeless (test_person.TestPerson.test_is_homeless)
      Проверка метода is_homeless. Если адрес - пустая строка, метод возвращает False ... 
        test_is_homeless (test_person.TestPerson.test_is_homeless) [address is "abc"]
      Проверка метода is_homeless. Если адрес - пустая строка, метод возвращает False ... ERROR
        test_is_homeless (test_person.TestPerson.test_is_homeless) [address is ""]
      Проверка метода is_homeless. Если адрес - пустая строка, метод возвращает False ... ERROR
        test_is_homeless (test_person.TestPerson.test_is_homeless) [address is ""]
      Проверка метода is_homeless. Если адрес - пустая строка, метод возвращает False ... ERROR
      test_set_address (test_person.TestPerson.test_set_address)
      Проверка сеттера адреса ... 
        test_set_address (test_person.TestPerson.test_set_address) [new address is ]
      Проверка сеттера адреса ... FAIL
        test_set_address (test_person.TestPerson.test_set_address) [new address is aaa]
      Проверка сеттера адреса ... FAIL
        test_set_address (test_person.TestPerson.test_set_address) [new address is bbb]
      Проверка сеттера адреса ... FAIL
      test_set_name (test_person.TestPerson.test_set_name)
      Проверка сеттера имени ... 
        test_set_name (test_person.TestPerson.test_set_name) [new name is a]
      Проверка сеттера имени ... FAIL
        test_set_name (test_person.TestPerson.test_set_name) [new name is aaa]
      Проверка сеттера имени ... FAIL
      
      ======================================================================
      ERROR: test_get_age (test_person.TestPerson.test_get_age) [year of birth is 1999]
      Проверка геттера возраста человека
      ----------------------------------------------------------------------
      Traceback (most recent call last):
        File "/home/vladimir/PycharmProjects/python_advanced/module_03_ci_culture_beginning/homework/hw4/test_person.py", line 20, in test_get_age
          answer: int = person.get_age()
                        ^^^^^^^^^^^^^^^^
        File "/home/vladimir/PycharmProjects/python_advanced/module_03_ci_culture_beginning/homework/hw4/person.py", line 9, in get_age
          now: datetime.datetime = datetime.datetime.now()
                                   ^^^^^^^^
      NameError: name 'datetime' is not defined. Did you forget to import 'datetime'
      
      ======================================================================
      ERROR: test_get_age (test_person.TestPerson.test_get_age) [year of birth is 1]
      Проверка геттера возраста человека
      ----------------------------------------------------------------------
      Traceback (most recent call last):
        File "/home/vladimir/PycharmProjects/python_advanced/module_03_ci_culture_beginning/homework/hw4/test_person.py", line 20, in test_get_age
          answer: int = person.get_age()
                        ^^^^^^^^^^^^^^^^
        File "/home/vladimir/PycharmProjects/python_advanced/module_03_ci_culture_beginning/homework/hw4/person.py", line 9, in get_age
          now: datetime.datetime = datetime.datetime.now()
                                   ^^^^^^^^
      NameError: name 'datetime' is not defined. Did you forget to import 'datetime'
      
      ======================================================================
      ERROR: test_get_age (test_person.TestPerson.test_get_age) [year of birth is 2024]
      Проверка геттера возраста человека
      ----------------------------------------------------------------------
      Traceback (most recent call last):
        File "/home/vladimir/PycharmProjects/python_advanced/module_03_ci_culture_beginning/homework/hw4/test_person.py", line 20, in test_get_age
          answer: int = person.get_age()
                        ^^^^^^^^^^^^^^^^
        File "/home/vladimir/PycharmProjects/python_advanced/module_03_ci_culture_beginning/homework/hw4/person.py", line 9, in get_age
          now: datetime.datetime = datetime.datetime.now()
                                   ^^^^^^^^
      NameError: name 'datetime' is not defined. Did you forget to import 'datetime'
      
      ======================================================================
      ERROR: test_is_homeless (test_person.TestPerson.test_is_homeless) [address is "abc"]
      Проверка метода is_homeless. Если адрес - пустая строка, метод возвращает False
      ----------------------------------------------------------------------
      Traceback (most recent call last):
        File "/home/vladimir/PycharmProjects/python_advanced/module_03_ci_culture_beginning/homework/hw4/test_person.py", line 64, in test_is_homeless
          self.assertEqual(person.is_homeless(), person.address != '')
                           ^^^^^^^^^^^^^^^^^^^^
        File "/home/vladimir/PycharmProjects/python_advanced/module_03_ci_culture_beginning/homework/hw4/person.py", line 28, in is_homeless
          return address is None
                 ^^^^^^^
      NameError: name 'address' is not defined. Did you mean: 'self.address'?
      
      ======================================================================
      ERROR: test_is_homeless (test_person.TestPerson.test_is_homeless) [address is ""]
      Проверка метода is_homeless. Если адрес - пустая строка, метод возвращает False
      ----------------------------------------------------------------------
      Traceback (most recent call last):
        File "/home/vladimir/PycharmProjects/python_advanced/module_03_ci_culture_beginning/homework/hw4/test_person.py", line 64, in test_is_homeless
          self.assertEqual(person.is_homeless(), person.address != '')
                           ^^^^^^^^^^^^^^^^^^^^
        File "/home/vladimir/PycharmProjects/python_advanced/module_03_ci_culture_beginning/homework/hw4/person.py", line 28, in is_homeless
          return address is None
                 ^^^^^^^
      NameError: name 'address' is not defined. Did you mean: 'self.address'?
      
      ======================================================================
      ERROR: test_is_homeless (test_person.TestPerson.test_is_homeless) [address is ""]
      Проверка метода is_homeless. Если адрес - пустая строка, метод возвращает False
      ----------------------------------------------------------------------
      Traceback (most recent call last):
        File "/home/vladimir/PycharmProjects/python_advanced/module_03_ci_culture_beginning/homework/hw4/test_person.py", line 64, in test_is_homeless
          self.assertEqual(person.is_homeless(), person.address != '')
                           ^^^^^^^^^^^^^^^^^^^^
        File "/home/vladimir/PycharmProjects/python_advanced/module_03_ci_culture_beginning/homework/hw4/person.py", line 28, in is_homeless
          return address is None
                 ^^^^^^^
      NameError: name 'address' is not defined. Did you mean: 'self.address'?
      
      ======================================================================
      FAIL: test_set_address (test_person.TestPerson.test_set_address) [new address is ]
      Проверка сеттера адреса
      ----------------------------------------------------------------------
      Traceback (most recent call last):
        File "/home/vladimir/PycharmProjects/python_advanced/module_03_ci_culture_beginning/homework/hw4/test_person.py", line 58, in test_set_address
          self.assertEqual(person.get_address(), new_address)
      AssertionError: 'abc' != ''
      - abc
      
      
      ======================================================================
      FAIL: test_set_address (test_person.TestPerson.test_set_address) [new address is aaa]
      Проверка сеттера адреса
      ----------------------------------------------------------------------
      Traceback (most recent call last):
        File "/home/vladimir/PycharmProjects/python_advanced/module_03_ci_culture_beginning/homework/hw4/test_person.py", line 58, in test_set_address
          self.assertEqual(person.get_address(), new_address)
      AssertionError: '' != 'aaa'
      + aaa
      
      
      ======================================================================
      FAIL: test_set_address (test_person.TestPerson.test_set_address) [new address is bbb]
      Проверка сеттера адреса
      ----------------------------------------------------------------------
      Traceback (most recent call last):
        File "/home/vladimir/PycharmProjects/python_advanced/module_03_ci_culture_beginning/homework/hw4/test_person.py", line 58, in test_set_address
          self.assertEqual(person.get_address(), new_address)
      AssertionError: '' != 'bbb'
      + bbb
      
      
      ======================================================================
      FAIL: test_set_name (test_person.TestPerson.test_set_name) [new name is a]
      Проверка сеттера имени
      ----------------------------------------------------------------------
      Traceback (most recent call last):
        File "/home/vladimir/PycharmProjects/python_advanced/module_03_ci_culture_beginning/homework/hw4/test_person.py", line 40, in test_set_name
          self.assertEqual(new_name, person.get_name())
      AssertionError: 'a' != 'Vova'
      - a
      + Vova
      
      
      ======================================================================
      FAIL: test_set_name (test_person.TestPerson.test_set_name) [new name is aaa]
      Проверка сеттера имени
      ----------------------------------------------------------------------
      Traceback (most recent call last):
        File "/home/vladimir/PycharmProjects/python_advanced/module_03_ci_culture_beginning/homework/hw4/test_person.py", line 40, in test_set_name
          self.assertEqual(new_name, person.get_name())
      AssertionError: 'aaa' != 'Sasha'
      - aaa
      + Sasha
      
      
      ----------------------------------------------------------------------
      Ran 6 tests in 0.022s
      
      FAILED (failures=5, errors=6)
  ## Исправленный файл (называется fixed_person.py)  
    """Исправленный файл person.py"""
      import datetime
      
      
      class Person:
          def __init__(self, name: str, year_of_birth: int, address: str = '') -> None:
              self.name: str = name
              self.yob: int = year_of_birth
              self.address: str = address
      
          def get_age(self) -> int:
              now: datetime.datetime = datetime.datetime.now()
              return now.year - self.yob
      
          def get_name(self) -> str:
              return self.name
      
          def set_name(self, name: str) -> None:
              self.name = name
      
          def set_address(self, address: str) -> None:
              self.address = address
      
          def get_address(self) -> str:
              return self.address
      
          def is_homeless(self) -> bool:
              """
              returns True if address is not set, false in other case
              """
              return self.address != ''
  ## Результаты unit тестов  
    test_get_address (test_fixed_person.TestPerson.test_get_address)
      Проверка геттера адреса ... ok
      test_get_age (test_fixed_person.TestPerson.test_get_age)
      Проверка геттера возраста человека ... ok
      test_get_name (test_fixed_person.TestPerson.test_get_name)
      Проверка геттера имени ... ok
      test_is_homeless (test_fixed_person.TestPerson.test_is_homeless)
      Проверка метода is_homeless. Если адрес - пустая строка, метод возвращает False ... ok
      test_set_address (test_fixed_person.TestPerson.test_set_address)
      Проверка сеттера адреса ... ok
      test_set_name (test_fixed_person.TestPerson.test_set_name)
      Проверка сеттера имени ... ok
      
      ----------------------------------------------------------------------
      Ran 6 tests in 0.024s
      
      OK
  