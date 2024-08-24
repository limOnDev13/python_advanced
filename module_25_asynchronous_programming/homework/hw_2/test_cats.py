import time
from typing import Callable

import async_cats_with_aiofiles.main as async_with_aiofiles
import async_cats_without_aiofiles.main as async_without_aiofiles
import process_cats.main as processes
import threads_cats.main as threads


def timer(func: Callable, name: str, *args) -> float:
    """Функция замеряет время работы переданной функции и пишет результат в stdout"""
    print(name)
    start = time.time()
    func(*args)
    return time.time() - start


def test(num_cats: int) -> list:
    funcs = ((async_with_aiofiles.main, 'async_with_aiofiles', num_cats),
             (async_without_aiofiles.main, 'async_without_aiofiles', num_cats),
             (processes.main, 'processes', num_cats),
             (threads.main, 'threads', num_cats))

    return [(func[1], timer(*func)) for func in funcs]


if __name__ == '__main__':
    tests: list[int] = [10, 50, 100, 150]
    results = [test(t) for t in tests]

    for result, num in zip(results, tests):
        print(f'{num=}')
        for timing in result:
            print(timing)

        print('*' * 30)
