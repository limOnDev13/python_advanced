import sqlite3


def get_answers() -> list:
    """Функция делает запросы в рамках одного подключения и собирает список ответов на вопросы из задания"""
    answers: list = list()
    tables_names: list[str] = [f'table_{num}' for num in range(1, 4)]

    with sqlite3.connect('hw_3_database.db') as conn:
        cursor = conn.cursor()

        # 1) Сколько записей (строк) хранится в каждой таблице?
        task_1_queries: list[str] = [f"""
        SELECT COUNT(*) FROM {table}
        """ for table in tables_names]

        task1_result: list = list()
        for query in task_1_queries:
            cursor.execute(query)
            task1_result.append(cursor.fetchone()[0])

        answers.append(task1_result)

        # 2) Сколько в таблице table_1 уникальных записей?
        task_2_query: str = """
        SELECT COUNT(DISTINCT id) FROM table_1
        """
        cursor.execute(task_2_query)
        answers.append(cursor.fetchone()[0])

        # 3) Как много записей из таблицы table_1 встречается в table_2?
        task_3_query: str = """
        SELECT COUNT(*) FROM
        (
        SELECT * FROM table_1
        INTERSECT
        SELECT * FROM table_2
        )
        """
        cursor.execute(task_3_query)
        answers.append(cursor.fetchone()[0])

        # 4) Как много записей из таблицы table_1 встречается и в table_2, и в table_3?
        task_4_query: str = """
        SELECT COUNT(*) FROM
        (
        SELECT * FROM table_1
        INTERSECT
        SELECT * FROM table_2
        INTERSECT
        SELECT * FROM table_3
        )
        """
        cursor.execute(task_4_query)
        answers.append(cursor.fetchone()[0])

        print(answers)
        return answers


def create_md_file_with_answers(answers: list, output_file: str = 'report.md') -> None:
    """
    Функция создает файл .md с ответами на вопросы из задания
    :param output_file: Имя output файла
    :param answers: Список ответов
    :return: None
    """
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write('## Задача 3. Анализ таблиц\n')

        for num, answer in enumerate(answers):
            output.write(f'{num + 1}. {answer}\n')


if __name__ == '__main__':
    create_md_file_with_answers(get_answers())
