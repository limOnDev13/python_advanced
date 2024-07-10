import sqlite3


def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        truck_number: str
) -> bool:
    get_hours_with_bad_temperature_query: str = """
    SELECT COUNT(*)
    FROM table_truck_with_vaccine
    WHERE truck_number = ? AND (temperature_in_celsius < 16 OR temperature_in_celsius > 20)
    """
    cursor.execute(get_hours_with_bad_temperature_query, (truck_number,))
    number_hours_in_bad_conditions, *_ = cursor.fetchone()

    return number_hours_in_bad_conditions > 3


if __name__ == '__main__':
    truck_number: str = input('Введите номер грузовика: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        spoiled: bool = check_if_vaccine_has_spoiled(cursor, truck_number)
        print('Испортилась' if spoiled else 'Не испортилась')
        conn.commit()
