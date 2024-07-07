from queue import PriorityQueue
import threading
from typing import Callable
from dataclasses import dataclass
import logging
import random
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOCK = threading.Lock()


@dataclass(order=True)
class Task:
    """Класс для хранения информации о задаче"""
    priority: int
    task: Callable
    args: tuple
    kwargs: dict


class Producer(threading.Thread):
    """
    Класс для генерации задач и добавления их в приоритетную очередь

    Args:
        priority_queue (PriorityQueue) - приоритетная очередь задач
    """
    count: int = 0  # Счетчик задач

    def __init__(self, priority_queue: PriorityQueue):
        super().__init__()
        self.queue = priority_queue
        logger.info('Producer: Старт работы')

    @classmethod
    def print_and_sleep(cls, *args, **kwargs) -> None:
        """Функция пишет в консоль args и kwargs и засыпает на случайное время"""
        logger.debug(f'args = {args}; kwargs = {kwargs}')
        time.sleep(random.uniform(0, 1))

    def generate_task(self):
        """Функция генерирует задачу с функцией print, которая принимает как args, так и kwargs"""
        while not self.queue.full():
            logger.info(f'Producer: Добавляю {self.count} задачу в очередь')

            priority: int = random.randint(0, 100)
            task: Task = Task(
                priority=priority,
                task=self.print_and_sleep,
                args=('Priority', 'is', priority),
                kwargs={'func': self.print_and_sleep()}
            )
            self.queue.put(task, block=False)

            Producer.count += 1

    def run(self):
        with LOCK:
            for _ in range(16):  # Количество логических потоков
                child_thread = threading.Thread(target=self.generate_task())
                child_thread.start()
        logger.info('Producer: Готово!')


class Consumer(threading.Thread):
    def __init__(self, priority_queue: PriorityQueue):
        super().__init__()
        self.queue = priority_queue
        logger.info('Consumer: Старт работы')

    def get_task(self):
        """Функция берет задачу из очереди и выполняет ее"""
        while not self.queue.empty():
            task = self.queue.get()

            logger.info(f'>running Task(priority={task.priority})')

            try:
                task.task(*task.args, **task.kwargs)
            except Exception as exc:
                logger.exception('Произошла ошибка при выполнении задачи', exc_info=exc)
            finally:
                self.queue.task_done()

    def run(self):
        with LOCK:
            for _ in range(16):  # кол-во логических потоков
                child_thread = threading.Thread(target=self.get_task)
                child_thread.start()

        logger.info('Consumer: Готово!')


if __name__ == '__main__':
    pr_queue = PriorityQueue(100)
    prod_thread: Producer = Producer(pr_queue)
    cons_thread: Consumer = Consumer(pr_queue)

    prod_thread.start()
    cons_thread.start()

    prod_thread.join()
    cons_thread.join()
