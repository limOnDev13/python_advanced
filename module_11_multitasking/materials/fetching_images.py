import logging
import os
import time
import threading
import multiprocessing
from typing import List

import requests

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

URL: str = 'https://cataas.com/cat'
OUT_PATH: str = 'temp/{}.jpeg'


def get_image(url: str, result_path: str) -> None:
    response: requests.Response = requests.get(url, timeout=(5, 5))
    if response.status_code != 200:
        return
    with open(result_path, 'wb') as ouf:
        ouf.write(response.content)


def load_images_sequential(number: int) -> None:
    start: float = time.time()
    for i in range(number):
        get_image(URL, OUT_PATH.format(i))
    logger.info('Done in {:.4}'.format(time.time() - start))


def load_images_multithreading(number: int) -> None:
    start: float = time.time()
    threads: List[threading.Thread] = []
    for i in range(number):
        thread = threading.Thread(target=get_image, args=(URL, OUT_PATH.format(i)))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    logger.info('Done in {:.4}'.format(time.time() - start))


def load_images_multiprocessing(number: int) -> None:
    start: float = time.time()
    procs: List[multiprocessing.Process] = []
    for i in range(number):
        proc = multiprocessing.Process(
            target=get_image,
            args=(URL, OUT_PATH.format(i)),
        )
        proc.start()
        procs.append(proc)

    for proc in procs:
        proc.join()

    logger.info('Done in {:.4}'.format(time.time() - start))


if __name__ == '__main__':
    if not os.path.exists('./temp'):
        os.mkdir('./temp')
    for number_images in range(1, 1050, 20):
        print(f'number_images = {number_images}')
        # load_images_sequential(number_images)
        load_images_multithreading(number_images)
        load_images_multiprocessing(number_images)
        time.sleep(1)
        print('-' * 30)
