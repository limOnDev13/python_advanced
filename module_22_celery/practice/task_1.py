import math
import time
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Callable, Tuple, Dict, Any


@dataclass(order=True)
class Task:
    priority: int
    func: Callable = field(compare=False)
    args: Tuple = field(default_factory=tuple, compare=False)
    kwargs: Dict = field(default_factory=dict, compare=False)

    def execute(self) -> None:
        self.func(*self.args, **self.kwargs)

    def __str__(self):
        task_str = self.func.__name__ + '('

        f_args = ', '.join(map(repr, self.args))
        task_str += f_args

        if self.kwargs:
            f_kwargs = ', '.join(
                f'{k}={v!r}' for k, v in self.kwargs.items()
            )
            task_str += ', ' + f_kwargs

        task_str += ')'
        return task_str


class TaskQueue:
    def __init__(self):
        self.queue = PriorityQueue()

    def add_task(self, task: Task) -> None:
        """Метод добавляет задачу в очередь с ее приоритетом. Чем ниже значение priority, тем приоритетнее задача"""
        print(f'Добавлена задача: {task}.')
        self.queue.put(task)

    def execute_tasks(self) -> None:
        while not self.queue.empty():
            task = self.queue.get()
            print('Исполняется задача:', task)
            task.execute()

            self.queue.task_done()

        self.queue.join()
        print('Все задачи были успешно выполнены')


def print_and_sleep(sec: int = 1):
    print(f'Засыпаю на {sec} сек')
    time.sleep(sec)
    print('Просыпаюсь')


if __name__ == '__main__':
    queue = TaskQueue()
    queue.add_task(Task(
        priority=3,
        func=print_and_sleep,
        args=(1,)
    ))
    queue.add_task(Task(
        priority=3,
        func=print,
        args=('Hello', 'World'),
        kwargs={'sep': '_'}
    ))
    queue.add_task(Task(
        priority=1,
        func=math.factorial,
        args=(50,)
    ))
    queue.execute_tasks()
