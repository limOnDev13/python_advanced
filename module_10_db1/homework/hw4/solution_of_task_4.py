import sqlite3


def get_answers() -> list:
    """Функция делает запросы в рамках одного подключения и собирает список ответов на вопросы из задания"""
    answers: list = list()

    with sqlite3.connect('hw_4_database.db') as conn:
        cursor = conn.cursor()

        # 1) Выяснить, сколько человек с острова N находятся за чертой бедности,
        # то есть получает меньше 5000 гульденов в год.
        task_1_query: str = """
        SELECT COUNT(*) FROM salaries
        WHERE salary < 5000
        """
        cursor.execute(task_1_query)
        answers.append(f'Количество людей за чертой бедности: {cursor.fetchone()[0]}')

        # 2) Посчитать среднюю зарплату по острову N.
        task_2_query: str = """
        SELECT ROUND(AVG(salary), 2) FROM salaries
        """
        cursor.execute(task_2_query)
        answers.append(f'Средняя зарплата по острову: {cursor.fetchone()[0]}')

        # 3) Посчитать медианную зарплату по острову.
        task_3_query_min_medium: str = """
        SELECT MAX(salary) FROM
        (SELECT salary FROM salaries ORDER BY salary LIMIT ROUND((SELECT COUNT(*) FROM salaries)) / 2)
        """
        cursor.execute(task_3_query_min_medium)
        min_medium = cursor.fetchone()[0]
        task_3_query_max_medium: str = """
        SELECT MIN(salary) FROM
        (SELECT salary FROM salaries ORDER BY salary DESC
         LIMIT ROUND((SELECT COUNT(*) FROM salaries)) / 2)
        """
        cursor.execute(task_3_query_max_medium)
        max_medium = cursor.fetchone()[0]
        answers.append(f'Медианная зарплата находится в интервале {(min_medium, max_medium)}')

        # 4) Посчитать число социального неравенства F, определяемое как F = T/K, где T — суммарный доход 10% самых
        # обеспеченных жителей острова N, K — суммарный доход остальных 90% людей.
        # Вывести ответ в процентах с точностью до двух знаков после запятой.
        task_4_query: str = """
        SELECT ROUND(100 * 
        (
            SELECT SUM(salary) FROM
            (
                SELECT salary FROM salaries ORDER BY salary DESC LIMIT 0.1 * (SELECT COUNT(*) FROM salaries)
            ) 
        )/(
            SELECT SUM(salary) FROM
            (
                SELECT salary FROM salaries ORDER BY salary LIMIT 0.9 * (SELECT COUNT(*) FROM salaries)
            )
        ), 2)
        """
        cursor.execute(task_4_query)
        answers.append(f'Число социального неравенства: {cursor.fetchone()[0]} %')

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
        output.write('## Задача 4. Исследование доходов населения\n')

        for num, answer in enumerate(answers):
            output.write(f'{num + 1}. {answer}\n')


if __name__ == '__main__':
    create_md_file_with_answers(get_answers())
