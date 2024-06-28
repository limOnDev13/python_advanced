from logger_helper import get_logger
from utils import string_to_operator
import logging.config
from logging_config import dict_config
import logging_tree


logging.config.dictConfig(dict_config)


app_logger = get_logger('app')


def calc(args):
    # print("Arguments: ", args)
    app_logger.debug(f"Arguments: {args}")

    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        # print("Error while converting number 1")
        # print(e)
        app_logger.exception('Error while converting number 1', exc_info=e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        # print("Error while converting number 1")
        # print(e)
        app_logger.exception('Error while converting number 1', exc_info=e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    # print("Result: ", result)
    # print(f"{num_1} {operator} {num_2} = {result}")
    app_logger.debug(f'Result: {result}')
    app_logger.info(f"{num_1} {operator} {num_2} = {result}")
    app_logger.error(f'Проверка фильтрации сообщения с не ASCII символами - ÎŒØ∏‡°⁄·°€йцукен')


if __name__ == '__main__':
    # Соберем дерево логгеров
    with open('logging_tree.txt', 'w', encoding='utf-8') as tree_file:
        tree_file.write(logging_tree.format.build_description())

    # calc(sys.argv[1:])
    calc('2+3')
    calc('2==3')
