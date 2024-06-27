from typing import Union, Callable
from operator import sub, mul, truediv, add
import logging.config
from logging_config import dict_config


utils_logger = logging.getLogger('utils')
logging.config.dictConfig(dict_config)


OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    if not isinstance(value, str):
        # print("wrong operator type", value)
        utils_logger.error(f'"wrong operator type", {value}')
        raise ValueError("wrong operator type")

    if value not in OPERATORS:
        # print("wrong operator value", value)
        utils_logger.error(f'"wrong operator type", {value}')
        raise ValueError("wrong operator value")

    return OPERATORS[value]
