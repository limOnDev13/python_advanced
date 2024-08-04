import sqlite3


def students_with_simple_teacher(cursor: sqlite3.Cursor) -> list[str]:
    """Функция находит учеников с самым простым учителем. Решение с подзапросом"""
    query: str = \
        f"""
        SELECT s.full_name
        FROM students s
        JOIN students_groups gr ON s.group_id = gr.group_id
        JOIN teachers t ON gr.teacher_id = t.teacher_id
        JOIN (
            SELECT avg(g.grade) as avg_grade, a.teacher_id t_id
            FROM assignments_grades g
            JOIN assignments a ON g.assignment_id = a.assignment_id
            GROUP BY a.teacher_id
        ) AS teachers_with_avg_grades ON t_id = t.teacher_id
        WHERE avg_grade = (SELECT max(avg_grade) FROM (
            SELECT avg(g.grade) as avg_grade, a.teacher_id t_id
            FROM assignments_grades g
            JOIN assignments a ON g.assignment_id = a.assignment_id
            GROUP BY a.teacher_id
        ))
        """
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]


if __name__ == '__main__':
    with sqlite3.connect('../../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        print(students_with_simple_teacher(cursor))
