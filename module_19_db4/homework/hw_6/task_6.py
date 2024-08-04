import sqlite3


def task_5(cursor: sqlite3.Cursor) -> list[tuple]:
    """Решение 5 задачи"""
    cursor.execute(
        """
        SELECT g.assignment_id, round(avg(g.grade), 2)
        FROM assignments_grades g
        JOIN assignments a ON g.assignment_id = a.assignment_id
        WHERE a.assignment_text LIKE '%прочитать%' OR a.assignment_text LIKE '%выучить%'
        GROUP BY g.assignment_id
        """
    )
    return cursor.fetchall()


if __name__ == '__main__':
    with sqlite3.connect('../../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        print('\t'.join(('id задания', 'средний балл')))
        for row in task_5(cursor):
            print('\t'.join(str(item) for item in row))
