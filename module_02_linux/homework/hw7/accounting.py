"""
Реализуйте приложение для учёта финансов, умеющее запоминать, сколько денег было потрачено за день,
а также показывать затраты за отдельный месяц и за целый год.

В программе должно быть три endpoints:

/add/<date>/<int:number> — сохранение информации о совершённой в рублях трате за какой-то день;
/calculate/<int:year> — получение суммарных трат за указанный год;
/calculate/<int:year>/<int:month> — получение суммарных трат за указанные год и месяц.

Дата для /add/ передаётся в формате YYYYMMDD, где YYYY — год, MM — месяц (от 1 до 12), DD — число (от 01 до 31).
Гарантируется, что переданная дата имеет такой формат и она корректна (никаких 31 февраля).
"""

from flask import Flask

app = Flask(__name__)

storage: dict[int, dict[int, int]] = dict()


@app.route("/add/<string:date>/<int:number>")
def add(date: str, number: int) -> tuple[str, int]:
    """
    Функция - эндпоинт. Сохраняет расходы, переданные через url в словарь
    :param date: Дата в формате YYYYMMDD
    :type date: str
    :param number: Количество затрат
    :type number: int
    :return: response status
    :rtype: tuple[str, int]
    """
    try:
        year: int = int(date[:4])
        month: int = int(date[4: 6])

        storage[year][month] = storage.setdefault(year, {}).setdefault(month, 0) + number
        return "Информация сохранена!", 200
    except Exception:
        return 'Какая-то ошибка!', 500


@app.route("/calculate/<int:year>")
def calculate_year(year: int) -> tuple[str, int]:
    """
    Функция - эндпоинт. Считает суммарные траты за год (передается через url) и возвращает результат
    :param year: Год
    :type year: int
    :return: Суммарные затраты за год
    :rtype: tuple[str, int]
    """
    return f'Траты за {year} равны {sum(storage.setdefault(year, {}).values())}', 200


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int) -> tuple[str, int]:
    """
    Функция - эндпоинт. Возвращает траты за указанный месяц указанного года
    :param year: Год
    :type year: int
    :param month: Месяц
    :type month: int
    :return: Суммарные затраты за месяц
    :rtype: tuple[str, int]
    """
    return f'Траты за {month} месяц {year} года равны {storage.setdefault(year, {}).setdefault(month, 0)}', 200


if __name__ == "__main__":
    app.run(debug=True)
