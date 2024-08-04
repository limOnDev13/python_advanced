import sqlite3


def count_overdue_assignments(cursor: sqlite3.Cursor) -> list[float, int, int]:
    """Функция считает среднее, макс и мин (в таком порядке) количество просроченных заданий для каждого класса"""
    cursor.execute(
        """
        SELECT group_id, round(avg(num), 2), max(num), min(num)
        FROM (
            SELECT s.group_id, count(s.group_id) num
            FROM assignments a
            JOIN assignments_grades g ON a.assignment_id = g.assignment_id
            JOIN students s ON s.student_id = g.student_id
            WHERE date(a.due_date) < date(g.date)
            GROUP BY g.assignment_id, s.group_id
            ORDER BY g.assignment_id, g.student_id
        )
        GROUP BY group_id
        """
    )
    return cursor.fetchall()


if __name__ == '__main__':
    with sqlite3.connect('../../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        print(count_overdue_assignments(cursor))
