import logging
import random
import threading
import time
from typing import List

TOTAL_TICKETS: int = 10
TOTAL_SEATS: int = 30
NUMBER_SELLERS: int = 4

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class Seller(threading.Thread):

    def __init__(self, barrier: threading.Barrier) -> None:
        super().__init__()
        self.barrier: threading.Barrier = barrier
        self.tickets_sold: int = 0
        logger.info('Seller started work')

    def run(self) -> None:
        global TOTAL_TICKETS
        while True:
            self.random_sleep()

            if TOTAL_TICKETS <= NUMBER_SELLERS:
                # Если осталось по одному билету на кассу - блокируем потоки, пока директор не добавит новые
                try:
                    self.barrier.wait()
                except threading.BrokenBarrierError:
                    logger.debug('A notification has been received from the barrier. The thread continues to work')

            self.tickets_sold += 1
            TOTAL_TICKETS -= 1
            logger.info(f'{self.name} sold one;  {TOTAL_TICKETS} left')
            logger.info(f'Seller {self.name} sold {self.tickets_sold} tickets')

    @classmethod
    def random_sleep(cls) -> None:
        time.sleep(random.randint(0, 1))


class Director(threading.Thread):
    def __init__(self, barrier: threading.Barrier):
        super().__init__()
        self.barrier = barrier
        logger.info('Director started work')

    def run(self):
        while True:
            if self.barrier.n_waiting < NUMBER_SELLERS:
                logger.debug(f'Number of threads pending is {self.barrier.n_waiting}')
                time.sleep(0.5)  # делаем задержку проверки, чтобы не нагружать процессор
            else:
                logger.debug(f'Number of threads pending is {self.barrier.n_waiting}')
                global TOTAL_TICKETS
                TOTAL_TICKETS += TOTAL_SEATS  # Добавляем билеты
                logger.info(f'Director added {TOTAL_SEATS} tickets')
                self.barrier.reset()  # Сбрасываем барьер
                logger.info('Director launched ticket offices')


def main() -> None:
    # Барьер будет ждать количество потоков равное количеству продавцов и директора
    barrier: threading.Barrier = threading.Barrier(NUMBER_SELLERS +2)
    sellers: List[Seller] = []
    for _ in range(4):
        seller = Seller(barrier)
        seller.start()
        sellers.append(seller)

    director: Director = Director(barrier)
    director.start()


if __name__ == '__main__':
    main()
