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

    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.tickets_sold: int = 0
        logger.info('Seller started work')

    def run(self) -> None:
        global TOTAL_TICKETS
        is_running: bool = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= NUMBER_SELLERS:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.name} sold one;  {TOTAL_TICKETS} left')
        logger.info(f'Seller {self.name} sold {self.tickets_sold} tickets')

    @classmethod
    def random_sleep(cls) -> None:
        time.sleep(random.randint(0, 1))


class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore):
        super().__init__()
        self.sem = semaphore

    def run(self):
        while True:
            global TOTAL_TICKETS
            if TOTAL_TICKETS > NUMBER_SELLERS:
                time.sleep(0.5)
                logger.debug(f'There are enough tickets for now - {TOTAL_TICKETS}')
            else:
                logger.debug(f'There are not enough tickets anymore - {TOTAL_TICKETS}')
                TOTAL_TICKETS += TOTAL_SEATS  # Добавляем билеты
                logger.info(f'Director added {TOTAL_SEATS} tickets')


def main() -> None:
    semaphore: threading.Semaphore = threading.Semaphore(NUMBER_SELLERS + 1)

    director: Director = Director(semaphore)
    director.start()

    sellers: List[Seller] = []
    for _ in range(4):
        seller = Seller(semaphore)
        seller.start()
        sellers.append(seller)


if __name__ == '__main__':
    main()
