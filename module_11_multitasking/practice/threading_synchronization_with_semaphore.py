import random
import threading
import time
from typing import Callable

from threading import Lock

COUNTER: int = 1
LOCK: threading.Lock = Lock()


class WorkerWithSemaphore(threading.Thread):
    def __init__(self, semaphore: threading.BoundedSemaphore, worker_func: Callable):
        super().__init__()
        self.sem = semaphore
        self.worker = worker_func

    def run(self):
        self.worker()


def worker_one() -> None:
    global COUNTER
    while COUNTER < 1000:
        COUNTER += 1

        print(f'Worker one incremented counter to {COUNTER}')
        sleep_time: int = random.randint(0, 1)
        # time.sleep(sleep_time)


def worker_two():
    global COUNTER
    while COUNTER > -1000:
        COUNTER -= 1

        print(f'Worker two decremented counter to {COUNTER}')
        sleep_time: int = random.randint(0, 1)
        # time.sleep(sleep_time)


def main():
    start = time.time()
    # thread_1 = threading.Thread(target=worker_one)
    # thread_2 = threading.Thread(target=worker_two)
    # thread_1.start()
    # thread_2.start()
    # thread_1.join()
    # thread_2.join()
    semaphore = threading.BoundedSemaphore(0)
    worker_1 = WorkerWithSemaphore(semaphore, worker_one)
    worker_2 = WorkerWithSemaphore(semaphore, worker_two)

    worker_1.start()
    worker_2.start()

    worker_1.join()
    worker_2.join()
    print('Execution time {:.4}'.format(time.time() - start))


if __name__ == '__main__':
    main()
