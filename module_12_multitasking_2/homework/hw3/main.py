import threading
from threading import Semaphore, Thread
import time
from typing import Callable


def custom_exception_hook(args):
    print(f'Говорит кастомный хук: {args}')


threading.excepthook = custom_exception_hook
sem: Semaphore = Semaphore()


def fun1():
    while True:
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)


def fun2():
    while True:
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)


t1: Thread = Thread(target=fun1)
t2: Thread = Thread(target=fun2)
t1.daemon = False
t2.daemon = False

try:
    t1.start()
    t2.start()
except KeyboardInterrupt:
    print('\nReceived keyboard interrupt, quitting threads.')
    exit(1)
