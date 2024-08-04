import sqlite3


def groups_info(cursor: sqlite3.Cursor) -> list[tuple]:
    query: str = """
SELECT gr_id, num_students, avg_grade
FROM
(
    SELECT s.group_id gr_id, count(s.student_id) num_students, round(avg(gr.grade), 2) avg_grade
    FROM students s
    JOIN assignments_grades gr ON s.student_id = gr.student_id
    GROUP BY gr_id
),
(
    SELECT count(sub_s.student_id) num_bad_students, sub_s.group_id bad_group_id
    FROM students sub_s
    WHERE sub_s.student_id NOT IN (
        SELECT sub_gr.student_id
        FROM assignments_grades sub_gr
    )
)
WHERE gr_id = bad_group_id
    """
    cursor.execute(
        """
SELECT gr_id, num_students, avg_grade, num_bad_students, num_late_students, num_students_with_retakes
FROM
-- Получаем количество человек в группе и средний балл
(
    SELECT s.group_id gr_id, count(s.student_id) num_students, round(avg(gr.grade), 2) avg_grade
    FROM students s
    JOIN assignments_grades gr ON s.student_id = gr.student_id
    GROUP BY gr_id
)
LEFT JOIN
-- Получаем количество студентов, которые ни разу не сдали работы
(
    SELECT count(sub_s.student_id) num_bad_students, sub_s.group_id bad_group_id
    FROM students sub_s
    WHERE sub_s.student_id NOT IN (
        SELECT sub_gr.student_id
        FROM assignments_grades sub_gr
    )
    GROUP BY bad_group_id
) ON gr_id = bad_group_id
LEFT JOIN
--Получаем количество людей, которые хоть раз опоздали со сдачей работы
(
    SELECT COUNT(DISTINCT g.student_id) num_late_students, s.group_id late_group_id
    FROM assignments_grades g
    JOIN assignments a ON a.assignment_id = g.assignment_id
    JOIN students s ON s.student_id = g.student_id
    WHERE date(g.date) > date(a.due_date)
    GROUP BY s.group_id
) ON bad_group_id = late_group_id
LEFT JOIN
-- Получаем количество повторных сдач
(
    SELECT retakes_group_id, count(retake_student_id) num_students_with_retakes
    FROM 
    (
        SELECT g.student_id retake_student_id, count(g.grade_id) num_retakes, s.group_id retakes_group_id
        FROM assignments_grades g
        JOIN students s ON g.student_id = s.student_id 
        GROUP BY g.student_id, g.assignment_id
        HAVING num_retakes > 1
    )
    GROUP BY retakes_group_id
) ON late_group_id = retakes_group_id
        """
    )
    return cursor.fetchall()


if __name__ == '__main__':
    with sqlite3.connect('../../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        print('\t'.join(('Номер группы', 'Кол-во студентов', 'Средний балл',
                         'Кол-во несдавших ни разу', 'Кол-во хоть раз опаздавших', 'Кол-во пересдававших')))
        for row in groups_info(cursor):
            print('  '.join((str(item) for item in row)))
