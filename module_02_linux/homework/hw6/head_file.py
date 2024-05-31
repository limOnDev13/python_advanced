"""
Реализуйте endpoint, который показывает превью файла, принимая на вход два параметра: SIZE (int) и RELATIVE_PATH —
и возвращая первые SIZE символов файла по указанному в RELATIVE_PATH пути.

Endpoint должен вернуть страницу с двумя строками.
В первой строке будет содержаться информация о файле: его абсолютный путь и размер файла в символах,
а во второй строке — первые SIZE символов из файла:

<abs_path> <result_size><br>
<result_text>

где abs_path — написанный жирным абсолютный путь до файла;
result_text — первые SIZE символов файла;
result_size — длина result_text в символах.

Перенос строки осуществляется с помощью HTML-тега <br>.

Пример:

/head_file/8/docs/simple.txt
/home/user/module_2/docs/simple.txt 8
hello wo

/head_file/12/docs/simple.txt
/home/user/module_2/docs/simple.txt 12
hello world!
"""

from flask import Flask
import os


app = Flask(__name__)


BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))


@app.route("/head_file/<int:size>/<path:relative_path>")
def head_file(size: int, relative_path: str) -> tuple[str, int]:
    """
    Функция - эндпоинт. Через url получает относительный путь к файлу и количество символов,
    которые необходимо прочитать. Это количество может превышать количество символов в файле.
    :param size: Количество символов, которые необходимо вывести
    :type size: int
    :param relative_path: Относительный путь до файла
    :type relative_path: str
    :return: Строку, с информацией о файле и первые size символов из этого файла
    :rtype: tuple[str, int]
    """
    file_path: str = os.path.join(BASE_DIR, relative_path)

    try:
        with open(file_path, 'r', encoding='utf-8') as in_file:
            text: str = in_file.read(size)

            return '{abs_path} {result_size}<br>{result_text}'.format(
                abs_path=file_path,
                result_size=len(text),
                result_text=text
            ), 200
    except FileNotFoundError:
        return 'Файл не найден', 404


if __name__ == "__main__":
    app.run(debug=True)
