import sqlite3


def best_students(cursor: sqlite3.Cursor, number: int = 10) -> list[tuple[str, float]]:
    query: str =\
        f"""
        SELECT s.full_name, round(avg(g.grade)) avg_grade
        FROM assignments_grades g
        JOIN students s ON g.student_id = s.student_id
        GROUP BY s.full_name
        ORDER BY avg_grade DESC
        LIMIT {number}
        """
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == '__main__':
    with sqlite3.connect('../../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        print(best_students(cursor))
