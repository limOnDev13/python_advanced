"""
В приложении для парольной аутентификации, которое мы рассматривали, недостаточно debug-сообщений. Добавим после каждой
строки с кодом в функции input_and_check_password ещё по debug-сообщению, например:
f"Мы создали объект hasher {hasher!r}"
после строки:
"hasher = hashlib.md5()"
"""

import getpass
import hashlib
import logging

logger = logging.getLogger("password_checker")


def input_and_check_password():
    logger.debug("Начало input_and_check_password")
    password: str = getpass.getpass()
    logger.debug('Пользователь ввел пароль')

    if not password:
        logger.warning("Вы ввели пустой пароль.")
        logger.debug('Пользователь ввел пустой пароль. input_and_check_password() вернула False')
        return False

    try:
        hasher = hashlib.md5()
        logger.debug('Создали hasher')

        hasher.update(password.encode("latin-1"))
        logger.debug('Выполнили команду hasher.update(password.encode("latin-1"))')

        if hasher.hexdigest() == "098f6bcd4621d373cade4e832627b4f6":
            logger.debug('Зашли в условие if hasher.hexdigest() == "098f6bcd4621d373cade4e832627b4f6"'
                         ' - input_and_check_password вернет True')
            return True
    except ValueError as ex:
        logger.debug('Попали в блок except ValueError as ex')
        logger.exception("Вы ввели некорректный символ ", exc_info=ex)

    logger.debug('Функция дошла до конца. input_and_check_password вернет False')
    return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Вы пытаетесь аутентифицироваться в Skillbox")
    count_number: int = 3
    logger.debug('Создали count_number: int = 3')
    logger.info(f"У вас есть {count_number} попыток")

    while count_number > 0:
        logger.debug('Зашли в блок while count_number > 0')
        if input_and_check_password():
            logger.debug('Зашли в блок if input_and_check_password(). Программа завершится с кодом 0')
            exit(0)
        count_number -= 1
        logger.debug('Уменьшили count_number на 1')

    logger.error("Пользователь трижды ввёл не правильный пароль!")
    logger.debug('Программа дошла до конца. Сейчас она завершится с кодом 1')
    exit(1)
