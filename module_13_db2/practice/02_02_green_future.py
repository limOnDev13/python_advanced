import sqlite3


def get_number_of_lucky_days(c: sqlite3.Cursor, month_number: int) -> float:
    parameter_like = f'%-{int(month_number)}-%' if month_number >= 10 else f'%-0{int(month_number)}-%'
    number_very_lucky_days_query: str = """
    SELECT COUNT(*)
    FROM (SELECT date, COUNT(action) AS count_al
          FROM table_green_future WHERE action = 'мешок алюминия' 
          GROUP BY date) AS al_table
    JOIN (SELECT date, COUNT(action) AS count_pl
          FROM table_green_future WHERE action = 'мешок пластика'
          GROUP BY date) AS pl_table
    ON al_table.date = pl_table.date
    JOIN (SELECT date, COUNT(action) AS count_man
          FROM table_green_future WHERE action = 'отнесли мешки на завод'
          GROUP BY date) as man_table
    ON al_table.date = man_table.date
    WHERE count_al >= 1 AND count_pl >= 2 AND count_man >= 1 AND al_table.date LIKE ?
    """
    c.execute(number_very_lucky_days_query, (parameter_like,))
    number_very_lucky_days, *_ = c.fetchone()

    number_days_in_month_query: str = """
    SELECT COUNT(date) FROM (SELECT date FROM table_green_future WHERE date LIKE ? GROUP BY date)
    """
    c.execute(number_days_in_month_query, (parameter_like, ))
    number_days_in_month, *_ = c.fetchone()

    return round(number_very_lucky_days * 100 / number_days_in_month, 5)


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        percent_of_lucky_days = get_number_of_lucky_days(cursor, 1)
        print(f"В ноябре у ребят было {percent_of_lucky_days:.02f}% удачных дня!")
