"""
1. Сконфигурируйте логгер программы из темы 4 так, чтобы он:

* писал логи в файл stderr.txt;
* не писал дату, но писал время в формате HH:MM:SS,
  где HH — часы, MM — минуты, SS — секунды с ведущими нулями.
  Например, 16:00:09;
* выводил логи уровня INFO и выше.

2. К нам пришли сотрудники отдела безопасности и сказали, что, согласно новым стандартам безопасности,
хорошим паролем считается такой пароль, который не содержит в себе слов английского языка,
так что нужно доработать программу из предыдущей задачи.

Напишите функцию is_strong_password, которая принимает на вход пароль в виде строки,
а возвращает булево значение, которое показывает, является ли пароль хорошим по новым стандартам безопасности.
"""

import getpass
import hashlib
import logging
import re


logger = logging.getLogger("password_checker")

ENGLISH_WORDS: set[str] = set()
WORDS_YET_LOADED: bool = False


def load_english_words() -> None:
    """
    Функция загружает английские слова из папки /usr/share/dict/words и сохраняет их в мн-во ENGLISH_WORDS
    :return: None
    """
    global WORDS_YET_LOADED
    if not WORDS_YET_LOADED:
        logger.debug('Загружаем слова')
        WORDS_YET_LOADED = True
        file_with_words: str = '/usr/share/dict/words'

        with open(file_with_words, 'r', encoding='utf-8') as file:
            for word in file:
                if len(word) > 4:
                    ENGLISH_WORDS.add(word.rstrip().lower())


def is_strong_password(password: str) -> bool:
    """
    Функция определяет, является ли пароль достаточно надежным согласно условию задачи
    :param password: Пароль
    :type password: str
    :return: True, если пароль прошел валидацию, иначе - False
    :rtype: bool
    """
    load_english_words()
    global ENGLISH_WORDS

    words_in_password: set[list[str]] = set(re.findall('[a-z]', password, flags=re.IGNORECASE))
    if words_in_password & ENGLISH_WORDS != {}:
        logger.debug('Нашли английское слово')
        return False
    return True


def input_and_check_password() -> bool:
    logger.debug("Начало input_and_check_password")
    password: str = getpass.getpass()

    if not password:
        logger.warning("Вы ввели пустой пароль.")
        return False
    elif not is_strong_password(password):
        logger.warning("Вы ввели слишком слабый пароль")
        return False

    try:
        hasher = hashlib.md5()

        hasher.update(password.encode("latin-1"))

        if hasher.hexdigest() == "098f6bcd4621d373cade4e832627b4f6":
            return True
    except ValueError as ex:
        logger.exception("Вы ввели некорректный символ ", exc_info=ex)

    return False


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        filename='stderr.txt',
        format='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%H:%M:%S',
        encoding='utf-8'
    )
    logger.info("Вы пытаетесь аутентифицироваться в Skillbox")
    count_number: int = 3
    logger.info(f"У вас есть {count_number} попыток")

    while count_number > 0:
        if input_and_check_password():
            exit(0)
        count_number -= 1

    logger.error("Пользователь трижды ввёл не правильный пароль!")
    exit(1)
