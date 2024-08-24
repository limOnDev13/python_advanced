from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

import requests
from pathlib import Path


URL = 'https://cataas.com/cat'
CATS_WE_WANT = 10
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


def get_cat(client: requests.Session) -> bytes:
    with client.get(URL) as response:
        print(response.status_code)
        result = response.content
        return result


def write_to_disk(content: bytes, idx: int):
    file_path = "{}/{}.png".format(OUT_PATH, idx)
    with open(file_path, mode='wb') as f:
        f.write(content)


def get_all_cats(num_cats: int):
    num_processes: int = cpu_count() * 5
    # Получим картинки по url
    with ThreadPool(processes=num_processes) as pool:
        with requests.Session() as client:
            images = pool.map_async(get_cat, [client for _ in range(num_cats)])
            pool.close()
            pool.join()
            images_bytes: list[bytes] = images.get(timeout=1)

    # Сохраним картинки на диск
    with ThreadPool(processes=num_processes) as pool:
        pool.starmap_async(write_to_disk, ((image, num) for image, num in zip(images_bytes, range(num_cats))))
        pool.close()
        pool.join()


def main(num_cats: int = CATS_WE_WANT):
    get_all_cats(num_cats)


if __name__ == '__main__':
    main()
