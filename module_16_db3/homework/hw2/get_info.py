import sqlite3


def task_1(cursor: sqlite3.Cursor) -> None:
    """Функция печатает информацию о заказе (задание 1)"""
    cursor.execute("""
    SELECT `manager`.full_name, `customer`.full_name, `order`.purchase_amount, `order`.date
    FROM `manager`, `customer`, `order`
    WHERE `order`.customer_id = `customer`.customer_id AND `order`.manager_id = `manager`.manager_id
    """)
    for row in cursor.fetchall():
        print(row)


def task_2(cursor: sqlite3.Cursor) -> None:
    """Функция печатает имена покупателей, не сделавших ни одной покупки (задание 2)"""
    cursor.execute("""
    SELECT full_name
    FROM `customer`
    WHERE customer_id NOT IN (SELECT customer_id FROM `order`)
    """)
    for row in cursor.fetchall():
        print(row)


def task_3(cursor: sqlite3.Cursor) -> None:
    """Функция выводит номер заказа, имена продавца и покупателя,
     если место жительства продавца и покупателя не совпадают. (задание 3)"""
    cursor.execute("""
    SELECT `order`.order_no, `manager`.full_name, `customer`.full_name
    FROM `order`
    JOIN `customer` ON `order`.customer_id = `customer`.customer_id
    JOIN `manager` ON `order`.manager_id = `manager`.manager_id
    WHERE `customer`.city != `manager`.city
    """)
    for row in cursor.fetchall():
        print(row)


def task_4(cursor: sqlite3.Cursor) -> None:
    """Функция выводит имена и номера заказов для покупателей,
     которые сделали заказ напрямую (без помощи менеджеров) (задание 4)"""
    cursor.execute("""
    SELECT `order`.order_no, `customer`.full_name
    FROM `order`
    JOIN `customer` ON `order`.customer_id = `customer`.customer_id
    WHERE `order`.manager_id IS NULL
    """)
    for row in cursor.fetchall():
        print(row)


def task_5(cursor: sqlite3.Cursor) -> None:
    """По желанию. Выведите имена уникальных пар покупателей, живущих в одном городе и имеющих одного менеджера."""
    cursor.execute(
        """       
        SELECT DISTINCT t1.full_name, t2.full_name
        FROM `customer` AS t1
        JOIN `customer` AS t2
        ON t1.city = t2.city AND t1.manager_id = t2.manager_id AND t1.full_name != t2.full_name
        GROUP BY t1.customer_id + t2.customer_id
        """
    )
    for row in cursor.fetchall():
        print(row)


if __name__ == '__main__':
    with sqlite3.connect('hw.db') as conn:
        c: sqlite3.Cursor = conn.cursor()
        # task_1(c)
        # task_2(c)
        # task_3(c)
        # task_4(c)
        task_5(c)
