import time
import random
import threading

import requests


def run():
    while True:
        requests.get("http://app:5000/hello_world", timeout=1)
        time.sleep(1)


if __name__ == '__main__':
    time.sleep(10)
    run()
