import threading
from threading import Semaphore, Thread
import time
import signal
import sys


def custom_exception_hook(args):
    print(f'Говорит кастомный хук: {args}')


threading.excepthook = custom_exception_hook
sem: Semaphore = Semaphore()
RUNNING: bool = True


def fun1():
    global RUNNING
    while RUNNING:
        sem.acquire()
        try:
            print(1)
        finally:
            sem.release()
        time.sleep(0.25)


def fun2():
    global RUNNING
    while RUNNING:
        sem.acquire()
        try:
            print(2)
        finally:
            sem.release()
        time.sleep(0.25)


def signal_handler(sig, frame):
    global RUNNING
    RUNNING = False
    print('Получен KeyboardInterrupt')


signal.signal(signal.SIGINT, signal_handler)

t1: Thread = Thread(target=fun1)
t2: Thread = Thread(target=fun2)

t1.start()
t2.start()

try:
    while t1.is_alive() or t2.is_alive():
        t1.join(timeout=1)
        t2.join(timeout=1)
except KeyboardInterrupt:
    RUNNING = False

    t1.join()
    t2.join()
    print('Почему-то эта строчка не выводится. Зачем тогда нужен блок try - except?')
print('Но эта строчка выводится...')   # обязательно прочитать в инете почему
