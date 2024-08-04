import sqlite3


def teacher_with_the_most_difficult_assignment(cursor: sqlite3.Cursor) -> tuple[str, float]:
    """Функция выводит ФИО учителя с самыми сложными заданиями и средним баллом"""
    query: str = \
        """
        SELECT round(avg(g.grade), 2) avg_grade, t.full_name
        FROM assignments_grades g
        JOIN assignments a ON g.assignment_id =  a.assignment_id
        JOIN teachers t ON a.teacher_id = t.teacher_id
        GROUP BY t.full_name
        ORDER BY avg_grade
        LIMIT 1
        """
    cursor.execute(query)
    return cursor.fetchone()


if __name__ == '__main__':
    with sqlite3.connect('../../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        print(teacher_with_the_most_difficult_assignment(cursor))
