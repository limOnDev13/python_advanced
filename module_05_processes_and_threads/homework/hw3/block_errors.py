"""
Реализуйте контекстный менеджер, который будет игнорировать переданные типы исключений, возникающие внутри блока with.
Если выкидывается неожидаемый тип исключения, то он прокидывается выше.
"""

from typing import Collection, Type, Literal
from types import TracebackType


class BlockErrors:
    """
    Контекстный менеджер. Принимает список исключений и игнорирует их внутри себя

    Args:
        errors (Collection) - исключения
    """
    def __init__(self, errors: Collection) -> None:
        self.errors: Collection = errors

    def __enter__(self) -> None:
        pass

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        if exc_type is not None and (exc_type in self.errors or issubclass(exc_type, tuple(self.errors))):
            return True
        elif exc_type is not None:
            raise exc_val


if __name__ == '__main__':
    err_types = {ZeroDivisionError, TypeError}
    with BlockErrors(err_types):
        a = 1 / 0
    print('Выполнено без ошибок')

