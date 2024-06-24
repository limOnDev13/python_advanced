"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""

from types import TracebackType
from typing import Type, Literal, IO
import sys
import traceback


class Redirect:
    """
    Контекстный менеджер. Позволяет перенаправить потоки stdout и stderr в IO объекты (уже открытые)

    Args:
        stdout (IO) - новый поток вывода
        stderr (IO) - новый поток вывода ошибок
    """
    def __init__(self, *, stdout: IO = None, stderr: IO = None) -> None:
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        self.new_stdout: IO = stdout
        self.new_stderr: IO = stderr

    def __enter__(self):
        """При заходе в к/м перенаправим потоки"""
        if self.new_stdout is not None:
            sys.stdout = self.new_stdout
        if self.new_stderr is not None:
            sys.stderr = self.new_stderr

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        """При выходе из к/м выведем ошибки (и завершим программу), перенаправим потоки в старые, а новые - закроем"""

        if exc_val is not None:
            sys.stderr.write(traceback.format_exc())

        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

        if self.new_stdout is not None:
            self.new_stdout.close()
        if self.new_stderr is not None:
            self.new_stderr.close()

        # По идее, если есть ошибка, то приложение должно отрубаться. Но в примере работа приложения продолжается,
        # поэтому этот блок закомментен
        # if exc_val is not None:
        #     sys.exit(1)
        return True


if __name__ == '__main__':
    with Redirect():
        raise ValueError

