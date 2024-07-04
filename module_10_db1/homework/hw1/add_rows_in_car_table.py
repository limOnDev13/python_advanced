import sqlite3


def insert_rows(rows: list[tuple[str, ...]]) -> None:
    """Функция построчно вставляет данные в таблицу table_car. В ide (community) не могу вставлять сразу несколько строк
    поэтому написал эту функцию"""
    with sqlite3.connect('hw_1_database.db') as conn:
        cursor = conn.cursor()

        # # 1) Подготовим данные. Столбец belongs_to связан со столбцом passport_id через FK
        # values: str = ',\n'.join(("('{num}', '{name}', '{description}', {belongs_to})".format(
        #     num=row[0],
        #     name=row[1],
        #     description=row[2],
        #     belongs_to=f"(SELECT passport_id FROM table_people WHERE name LIKE '%{row[3].split()[0]}%')"
        # ) for row in rows
        # ))
        # print(f"INSERT INTO table_car (car_number, name, description, belongs_to) VALUES"
        #       f"\n{values}\n")
        # cursor.execute(f"INSERT INTO table_car (car_number, name, description, belongs_to) VALUES\n"
        #                f"({values})")

        insert_query = """
        INSERT INTO table_car (car_number, name, description, belongs_to)
        VALUES (?, ?, ?, (SELECT passport_id FROM table_people WHERE name LIKE ?))
        """
        records: list[list[str]] = [[row[0], row[1], row[2], '%' + row[3].split()[0] + '%']
                                    for row in rows]
        cursor.executemany(insert_query, records)


def get_rows_from_readme() -> list[tuple[str, ...]]:
    """Функция считывает строки для таблицы из файла README.md и возвращает их в виде списка кортежей"""
    rows: list[tuple[str, ...]] = list()

    with open('README.md', 'r', encoding='utf-8') as file:
        for line in file:
            if '|' in line:
                row_data: list[str] = line.split('|')
                row: tuple[str, ...] = tuple(column.lstrip().rstrip()
                                             for num, column in enumerate(row_data) if 1 < num < 6)

                rows.append(row)

    return rows[2:]


if __name__ == '__main__':
    insert_rows(get_rows_from_readme())
