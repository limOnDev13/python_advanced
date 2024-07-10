import sqlite3

ivan_salary_query: str = """
SELECT salary FROM table_effective_manager WHERE name = 'Иван Совин'
"""
with sqlite3.connect('../homework.db') as conn:
    cursor = conn.cursor()
    cursor.execute(ivan_salary_query)
    IVAN_SALARY, *_ = cursor.fetchone()


def delete_employee(cursor: sqlite3.Cursor, name: str) -> None:
    """Функция удаляет запись о сотруднике"""
    delete_query: str = """
    DELETE FROM table_effective_manager
    WHERE name = ?
    """
    print(f'Уволить {name}')
    cursor.execute(delete_query, (name,))


def increase_salary(cursor: sqlite3.Cursor, name: str) -> None:
    """Функция повышает зарплату сотруднику"""
    update_query: str = """
    UPDATE table_effective_manager
    SET salary = (SELECT salary FROM table_effective_manager WHERE name = ?) * 1.1
    WHERE name = ?
    """
    print(f'Повысить зарплату {name}')
    cursor.execute(update_query, (name, name))


def ivan_sovin_the_most_effective(
        cursor: sqlite3.Cursor,
        name: str,
) -> None:
    select_salary_query: str = """
    SELECT salary FROM table_effective_manager WHERE name = ?
    """
    cursor.execute(select_salary_query, (name,))
    current_salary, *_ = cursor.fetchone()

    if current_salary * 1.1 > IVAN_SALARY:
        delete_employee(cursor, name)
    else:
        increase_salary(cursor, name)


if __name__ == '__main__':
    name: str = input('Введите имя сотрудника: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        ivan_sovin_the_most_effective(cursor, name)
        conn.commit()
