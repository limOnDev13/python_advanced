import sqlite3
import datetime
from typing import Generator


SPORTS: tuple[str, ...] = (
    'футбол', 'хоккей', 'шахматы', 'SUP сёрфинг', 'бокс', 'Dota2', 'шах-бокс'
)


def check_how_many_workers_involved() -> int:
    """Функция считает сколько сотрудников было задействовано в течение года"""
    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()
        select_query: str = """
        SELECT COUNT(*) FROM (SELECT employee_id FROM table_friendship_schedule GROUP BY employee_id)"""
        cursor.execute(select_query)
        number_workers, *_ = cursor.fetchone()

        return number_workers


def get_workers_today(cursor: sqlite3.Cursor, day: int, required_num_workers: int = 10):
    """
    Функция - генератор. Сначала получает список людей, доступных на переданный день недели,
    а после выдает каждые десять человек по кругу
    :param cursor: Курсор
    :param day: Номер дня недели (0 - понедельник, 1 - вторник и т.д.)
    :param required_num_workers: Необходимое количество людей для смены
    :return: Список id работников, которые выйдут в смену
    """
    # Получим список доступных людей на данный день
    select_available_workers_query: str = """
    SELECT id FROM table_friendship_employees WHERE preferable_sport != ?
    """
    cursor.execute(select_available_workers_query, (SPORTS[day],))
    available_workers = cursor.fetchall()
    current_index: int = 0

    # Возвращаем required_num_workers человек из списка по кругу
    while True:
        yield available_workers[current_index: current_index + required_num_workers]
        current_index = (current_index + 1 + day) % len(available_workers)


def update_work_schedule(cursor: sqlite3.Cursor, year: int = 2020, required_num_workers: int = 10) -> None:
    """Принцип такой же как и у составленного заранее расписания (которое не учитывает спорт),
    только для каждого дня недели соберем множество доступных работников
    и будем брать по кругу 10 человек из этого множества"""
    # Сбросим данные расписания
    delete_query: str = """DELETE FROM table_friendship_schedule"""
    cursor.execute(delete_query)

    # Пробежимся по каждой дате в году и добавим рабочих в расписание
    start_date: datetime.date = datetime.date(year=year, month=1, day=1)
    end_date: datetime.date = datetime.date(year=year, month=12, day=31)
    current_date: datetime.date = start_date
    # Соберем генераторы работников по дням недели
    generators_of_workers: list[Generator] = [get_workers_today(cursor, day, required_num_workers) for day in range(7)]

    while current_date <= end_date:
        insert_query: str = """
        INSERT INTO table_friendship_schedule (employee_id, date)
        VALUES (?, ?)
        """
        weekday: int = current_date.weekday()
        ids = generators_of_workers[weekday].__next__()
        print(f'Дата: {current_date}; день недели: {weekday}; ids: {ids}')

        input_data: list[tuple[str, str]] = [
            (employee_id[0], current_date.strftime('%Y-%m-%d'))
            for employee_id in ids]

        cursor.executemany(insert_query, input_data)
        current_date = current_date + datetime.timedelta(days=1)


if __name__ == '__main__':
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        update_work_schedule(cursor)
        conn.commit()

    print(f'За год отработало {check_how_many_workers_involved()} сотрудников')
