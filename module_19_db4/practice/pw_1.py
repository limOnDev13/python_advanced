import sqlite3


def search_grades(cursor: sqlite3.Cursor) -> tuple[float, int, int]:
    """Функция находит среднюю, максимальную и минимальную оценки в таблице assignments_grades"""
    # Средняя оценка
    cursor.execute(
        """
        SELECT round(avg(grade), 2), max(grade), min(grade) FROM assignments_grades
        """
    )
    return cursor.fetchone()


def num_members(cursor: sqlite3.Cursor) -> tuple[int, int]:
    """Функция находит количество учеников и учителей в таблицах students и teachers"""
    """
    SELECT count(students.student_id) as num_students, count(teachers.teacher_id) as num_teachers
    FROM students, teachers
    """
    cursor.execute(
        """
        SELECT *
        FROM (SELECT count(*) as num_s FROM students), (SELECT count(*) as num_t FROM teachers)
        """
    )
    return cursor.fetchone()


if __name__ == '__main__':
    with sqlite3.connect('homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        print(search_grades(cursor))
        print(num_members(cursor))
