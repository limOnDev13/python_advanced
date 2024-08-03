import sqlite3


def max_avg_grade(cursor: sqlite3.Cursor) -> tuple[int, float]:
    """Функция возвращает максимальный средний бал группы и номер этой группы"""
    cursor.execute(
        """
        SELECT round(max(avg_grade), 2), group_id
        FROM (
        SELECT avg(g.grade) avg_grade, s.group_id group_id
        FROM assignments_grades g
        JOIN students s
        ON g.student_id = s.student_id
        GROUP BY s.group_id
        )
        """
    )
    return cursor.fetchone()


def num_students_in_groups(cursor: sqlite3.Cursor) -> list[tuple[int, int]]:
    """Функция выводит список количеств учеников в каждой группе"""
    cursor.execute(
        """
        SELECT count(student_id), group_id
        FROM students
        GROUP BY group_id
        """
    )
    return cursor.fetchall()


if __name__ == '__main__':
    with sqlite3.connect('homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        print(max_avg_grade(cursor))
        print(num_students_in_groups(cursor))
