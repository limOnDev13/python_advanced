"""
Хорошим паролем считается пароль, в котором есть
как минимум восемь символов, большие и маленькие буквы,
а также как минимум одна цифра и один символ из списка

!@#$%^&*()-+=_

Сделайте так, чтобы при вводе пароля проверялось, является ли пароль хорошим.
И если нет — предупредите пользователя (с помощью warning, конечно), что введённый пароль слабый.
В идеале ещё и объясните почему.
"""
import getpass
import hashlib
import logging
import re

logger = logging.getLogger("password_checker")


def check_password_difficulty(password: str) -> bool:
    """
    Функция проверяет сложность введенного пароля согласно условию задачи
    :param password: пароль
    :return: True, если пароль достаточно сложный
    """
    # длина пароля => 8
    if len(password) < 8:
        return False
    # есть большие буквы
    if not re.search(r'[A-Z]', password):
        return False
    # есть маленькие буквы
    if not re.search(r'[a-z]', password):
        return False
    # есть цифры
    if not re.search(r'\d', password):
        return False
    # есть спец символ
    if not re.search(r'[!@#$%^&*()-+=_]', password):
        return False
    return True


def input_and_check_password():
    logger.debug("Начало input_and_check_password")
    password: str = getpass.getpass()
    print(password)

    while not check_password_difficulty(password):
        logger.warning('Вы ввели недостаточно сложный пароль')
        password = getpass.getpass()

    if not password:
        logger.warning("Вы ввели пустой пароль.")
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
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Вы пытаетесь аутентифицироваться в Skillbox")
    count_number: int = 0

    while True:
        try:
            count_number = int(input('Сколько раз вы хотите вводит пароль? (минимум - 2, максимум - 10) '))

            if not 2 <= count_number <= 10:
                raise ValueError
        except ValueError:
            logger.warning('Пожалуйста, введите число от 2 до 10!')
        else:
            break
    logger.info(f"У вас есть {count_number} попыток")

    while count_number > 0:
        if input_and_check_password():
            exit(0)
        count_number -= 1

    logger.error("Пользователь трижды ввёл не правильный пароль!")
    exit(1)
