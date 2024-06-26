"""
У нас есть кнопочный телефон (например, знаменитая Nokia 3310), и мы хотим,
чтобы пользователь мог проще отправлять СМС. Реализуем своего собственного клавиатурного помощника.

Каждой цифре телефона соответствует набор букв:
* 2 — a, b, c;
* 3 — d, e, f;
* 4 — g, h, i;
* 5 — j, k, l;
* 6 — m, n, o;
* 7 — p, q, r, s;
* 8 — t, u, v;
* 9 — w, x, y, z.

Пользователь нажимает на клавиши, например 22736368, после чего на экране печатается basement.

Напишите функцию my_t9, которая принимает на вход строку, состоящую из цифр 2–9,
и возвращает список слов английского языка, которые можно получить из этой последовательности цифр.
"""
from typing import List, Optional, Callable, Any
from copy import deepcopy
import re
import time
import functools


T9_DICT: dict[str, str] = {
    '2': 'abc',
    '3': 'def',
    '4': 'ghi',
    '5': 'jkl',
    '6': 'mno',
    '7': 'pqrs',
    '8': 'tuv',
    '9': 'wxyz'
}
WORDS: set[str] = set()
MIN_LEN_TO_CHECK: int = 4


def load_words() -> None:
    """Функция загружает английские слова в множество WORDS"""
    with open('/usr/share/dict/words', 'r', encoding='utf-8') as file:
        for line in file:
            WORDS.add(line.rstrip().lower())


def timer(func: Callable) -> Callable:
    """Функция - декоратор. Показывает время работы функции"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time: float = time.time()
        result: Any = func(*args, **kwargs)
        print(f'Время работы {func.__name__}: {round(time.time() - start_time, 5)}')
        return result
    return wrapper


def my_t9(input_numbers: str) -> List[str]:
    """
    Функция T9. Получает строку чисел (цифры от 2 до 9) и выводит подходящие английские слова согласно условию задачи
    :param input_numbers: Строка чисел
    :type input_numbers: str
    :return: Список подходящих слов
    :rtype: list[str]
    """
    # Слова будем подбирать рекурсивно
    # Чтобы получилась рекурсия, можно отправлять не только цифры, но и буквы
    result_words: list[str] = list()

    t9_code: Optional[re.Match] = re.match(r'([a-z]*)(\d)(.*)', input_numbers)
    # Условие остановки рекурсии - все цифры заменены на буквы
    if t9_code is None:
        return [word for word in WORDS if word.startswith(input_numbers)]
    else:
        first_word_part: str = t9_code.group(1)
        # комбинации букв длиннее MIN_LEN_TO_CHECK можно сразу проверять,
        # чтобы на начальных итерациях отсеять неподходящие комбинации
        if (len(first_word_part) >= MIN_LEN_TO_CHECK and
                [word for word in WORDS if word.startswith(first_word_part)] == []):
            return []

        number: str = t9_code.group(2)
        last_word_part: str = t9_code.group(3)

        # рекурсия
        for letter in T9_DICT[number]:
            result_words.extend(my_t9(''.join((first_word_part, letter, last_word_part))))

        return result_words


def t9_with_deleting_words(input_numbers: str, used_words: Optional[set[str]] = None) -> list[str]:
    """
    Функция т9. Работает аналогично my_t9, но по другому принципу. Вместо того,
    чтобы шерстить каждый раз все известные слова, функция отсекает слова,
    которые не начинаются на комбинации переданных букв, и шерстит урезанный список слов
    :param input_numbers: Строка чисел
    :type input_numbers: str
    :param used_words: Множество слов, среди которых ищутся подходящие
    :type used_words: Optional[set[str]]
    :return: Список подходящих слов
    :rtype: list[str]
    """
    # Алгоритм работает практически также, как и my_t9 с небольшими изменениями
    if used_words is None:
        used_words = deepcopy(WORDS)  # нужно для первой итерации
    elif used_words == {}:  # если передалось пустое множество, то искать нет смысла
        return []

    result_worlds: list[str] = list()

    t9_code: Optional[re.Match] = re.match(r'([a-z]*)(\d)(.*)', input_numbers)
    if t9_code is None:
        # Возвращаем подходящие слова из used_words
        return [word for word in used_words if word.startswith(input_numbers)]
    else:
        first_word_part: str = t9_code.group(1)
        if (len(first_word_part) >= MIN_LEN_TO_CHECK and
                [word for word in used_words if word.startswith(first_word_part)] == []):
            return []
        number: str = t9_code.group(2)
        last_word_part: str = t9_code.group(3)

        for letter in T9_DICT[number]:
            result_worlds.extend(t9_with_deleting_words(
                first_word_part + letter + last_word_part,
                {word for word in used_words if word.startswith(first_word_part + letter)}))  # отсекаем лишние слова

        return result_worlds


def check_algorythm_are_equals(algorithms: list[Callable]) -> None:
    """
    Функция для проверки всех алгоритмов t9 - необязательно смотреть, этого нет в задании
    :param algorithms: список алгоритмов т9
    :return: None
    """
    test_strings: list[str] = [
        '22736368',
        '2',
        '23',
        '234',
        '2345',
        '23456',
        '2' * 10,
        '2' * 11,
        '2' * 12,
        '2' * 15,
        '2' * 20,
        '2' * 25,
        '2' * 30,
        '23456789'
    ]
    # Пробежимся по всем тестам и алгоритмов и красиво запишем результат в терминал
    for test_input in test_strings:
        standart = algorithms[0](test_input)
        print(f'test input: {test_input}')
        for algorithm in algorithms:
            algorithm_result = algorithm(test_input)
            print(f'{algorithm.__name__} is OK? {set(algorithm_result) == set(standart)}')
            if set(algorithm_result) != set(standart):
                print(standart)
                print(algorithm_result)
        print('-' * 30)


if __name__ == '__main__':
    load_words()

    numbers: str = input('Введите числа без пробела\n')
    words: List[str] = timer(my_t9)(numbers)
    print(*words, sep='\n')

    # words = timer(t9_with_deleting_words)(numbers)
    # print(*words, sep='\n')

    # Проверка алгоритмов
    # check_algorythm_are_equals([timer(my_t9), timer(t9_with_deleting_words)])
    """
    Смог придумать только 2 алгоритма Т9 - my_t9 и t9_with_deleting_words. Второй алгоритм практически всегда работает 
    быстрее чем первый, за исключением тех случаев, когда количество вводимых цифр очень мало (1, 2, 3).
    За счет параметра MIN_LEN_TO_CHECK скорость алгоритмов заметно возросла, т.к. отпала проверять длинные комбинации
    букв, которые точно не являются частью слов. Но этот параметр не панацея, так как поиск длинных слов замедляется
    за счет того, что количество проверок увеличивается. Наверное, можно придумать какой-нибудь способ сделать этот
    параметр адаптивным к длине слова, но я пока не придумал и оставил константой.
    Решением этой задачи пусть будет my_t9, весь остальной код - проба пера.
    """
