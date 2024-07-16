import sqlite3
from typing import Optional


TEST_DATA: list[dict] = [
    {'floor': 1, 'beds': 2, 'guestNum': 3, 'price': 4},
    {'floor': 2, 'beds': 3, 'guestNum': 4, 'price': 5},
    {'floor': 3, 'beds': 4, 'guestNum': 5, 'price': 6},
    {'floor': 4, 'beds': 5, 'guestNum': 6, 'price': 7},
]
REF_GET_ROOMS: dict = {'ref': 'http://loacalhost:5000/rooms',
                       'description': 'Посмотреть информацию об имеющихся комнатах'}
REF_ADD_NEW_ROOM: dict = {'ref': 'http://localhost:5000/add_new_room', 'description': 'Добавить новую комнату'}
REF_BOOKING: dict = {'ref': 'http://localhost:5000/booking', 'description': 'Забронировать комнату'}


def create_db() -> None:
    """Функция создает базу данных и таблицу для бронирования номеров отеля"""
    with sqlite3.connect('booking.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='booking'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE IF NOT EXISTS `rooms` (
                    roomId INTEGER PRIMARY KEY AUTOINCREMENT,
                    floor INTEGER NOT NULL,
                    beds INTEGER NOT NULL,
                    guestNum INTEGER NOT NULL,
                    price INTEGER NOT NULL
                );
                """
            )
            cursor.executescript(
                """
                CREATE TABLE IF NOT EXISTS booking (
                    orderId INTEGER PRIMARY KEY AUTOINCREMENT,
                    roomId INTEGER,
                    checkIn INTEGER NOT NULL,
                    checkOut INTEGER NOT NULL,
                    first_name TEXT NOT NULL,
                    second_name TEXT NOT NULL,
                    FOREIGN KEY (roomId) REFERENCES rooms (roomId)
                );
                """
            )


def add_new_room(floor: int, beds: int, guest_num: int, price: int) -> None:
    """Функция добавляет информацию о комнате в бд"""
    with sqlite3.connect('booking.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO rooms (floor, beds, guestNum, price) VALUES (?, ?, ?, ?)
            """, (floor, beds, guest_num, price)
        )


def get_info_about_all_rooms() -> dict:
    """Функция возвращает всю информацию о комнатах из бд в виде словаря"""
    with sqlite3.connect('booking.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM `rooms`
            """
        )
        result = cursor.fetchall()
        return {'rooms': [{'roomId': row[0], 'floor': row[1], 'beds': row[2], 'guestNum': row[3], 'price': row[4]}
                for row in result],
                'refs': [REF_ADD_NEW_ROOM, REF_BOOKING]
                }


def get_info_about_rooms_between_dates_with_guests_num(
        check_in: int, check_out: int, guest_num: Optional[int] = None) -> dict:
    """Функция возвращает информацию о комнатах, которые свободны между датами check_in и check_out включительно
    с переданным количеством гостей (если количество - None, то любое количество)"""
    with sqlite3.connect('booking.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        if guest_num is not None:
            cursor.execute(
                """
                SELECT * FROM rooms
                WHERE roomId NOT IN (SELECT roomId FROM booking WHERE NOT (checkIn > ? OR checkOut < ?))
                AND guestNum = ?
                """, (check_out, check_in, guest_num)
            )
        else:
            cursor.execute(
                """
                SELECT * FROM rooms
                WHERE roomId NOT IN (SELECT roomId FROM booking WHERE NOT (checkIn > ? OR checkOut < ?))
                """, (check_out, check_in)
            )
        result = cursor.fetchall()
        return {'rooms': [{'roomId': row[0], 'floor': row[1], 'beds': row[2], 'guestNum': row[3], 'price': row[4]}
                          for row in result],
                'refs': [REF_ADD_NEW_ROOM, REF_BOOKING]
                }


def booking(check_in: int, check_out: int, first_name: str, second_name: str, room_id: int) -> bool:
    """Функция добавляет новую бронь в таблицу booking"""
    # Проверим, что комната не забронирована
    free_rooms: dict = get_info_about_rooms_between_dates_with_guests_num(check_in, check_out)
    if room_id not in [row['roomId'] for row in free_rooms['rooms']]:
        return False

    with sqlite3.connect('booking.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO booking (checkIn, checkOut, first_name, second_name, roomID)
            VALUES (?, ?, ?, ?, ?)
            """, (check_in, check_out, first_name, second_name, room_id)
        )
        return True


def id_in_rooms(room_id: int) -> bool:
    """Функция возвращает True, если room_id есть в таблице rooms, иначе - False"""
    with sqlite3.connect('booking.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT EXISTS(SELECT * FROM rooms WHERE roomId = ?)
            """, (room_id,)
        )
        return bool(cursor.fetchone()[0])
