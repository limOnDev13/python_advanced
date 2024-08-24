import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import aiofiles


NETLOCS: set = set()


async def get_refs(client: aiohttp.ClientSession, init_ref: str) -> set[str]:
    """Функция возвращает список внешних ссылок по адресу init_ref"""
    external_refs: set[str] = set()
    parsed_url = urlparse(init_ref)
    netloc: str = parsed_url.netloc
    scheme: str = parsed_url.scheme
    print(init_ref)

    try:
        async with client.get(init_ref) as response:
            # Получим страницы с 2xx статусами
            if 200 <= response.status < 300:
                html = await response.read()
                bs = BeautifulSoup(html, 'lxml')

                for href in bs.find_all('a', href=True):
                    # Получим тег href
                    match = re.search(r'href="(.*?)"', str(href))
                    if match:
                        ref = match.group(1)
                        ref_netloc = urlparse(ref).netloc
                        # Выбросим внутренние ссылки (и, соответственно, относительные) и домены, которые уже посещали
                        if netloc in ref or scheme not in ref or ref_netloc in NETLOCS:
                            continue
                        else:
                            # Если ссылка ведет на ранее не посещенный сайт, добавим ее в результат,
                            # а ее netloc - в NETLOCS
                            external_refs.add(ref)
                            NETLOCS.add(ref_netloc)
                return external_refs
    except:
        return set()


async def crawler(client: aiohttp.ClientSession,
                  init_refs: set[str], cur_depth: int = 0, max_depth: int = 3) -> set[str]:
    """Функция асинхронно парсит внешние ссылки из полученных init_refs. cur_depth - текущая глубина рекурсии,
     max_depth - максимальная"""
    # Если глубина парсинга равна максимальной - вернем полученное множество
    if cur_depth >= max_depth:
        return init_refs
    # Если получили пустое множество - вернем его
    if not init_refs:
        return set()

    set_refs: set = init_refs.copy()

    # Создадим список задач по парсингу внешних ссылок
    tasks = [get_refs(client, ref) for ref in init_refs]
    result_sets = await asyncio.gather(*tasks)
    # Не могу понять, откуда берутся None в result_sets
    for result_set in result_sets:
        if result_set:
            set_refs = set_refs.union(result_set)
        req_refs = await crawler(client, result_set, cur_depth + 1, max_depth)
        if req_refs:
            set_refs = set_refs.union(req_refs)
    return set_refs


async def write_to_disk(file: str, urls: set[str]):
    async with aiofiles.open(file, 'w') as f:
        for url in urls:
            await f.write(f'{url}\n')


async def main(init_refs, output_file: str = 'result_urls.txt'):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as client:
        refs_set: set[str] = await crawler(client, init_refs)
        for ref in refs_set:
            print(ref)

        await write_to_disk(output_file, refs_set)


if __name__ == '__main__':
    asyncio.run(main({'https://ya.ru/', 'https://www.google.ru/', 'https://skillbox.ru/'}))
