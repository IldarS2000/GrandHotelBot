from psycopg2 import OperationalError
from psycopg2 import sql, pool
from database.config import *

connection_pool = pool.SimpleConnectionPool(10, 50,
                                            database=database,
                                            user=user,
                                            password=password,
                                            host=host,
                                            port=port)


def _execute_query(connection, query, params):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def _execute_read_query(connection, query, params):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def vacant_room(type, count, arrival_date, departure_date):
    con = connection_pool.getconn()
    select_vacant = "select * from vacant_room(%s,%s,%s,%s)"
    params = [type, count, arrival_date, departure_date]
    result = _execute_read_query(con, select_vacant, params)
    connection_pool.putconn(con)
    return result


def description(room_number):
    con = connection_pool.getconn()
    select_description = "select description from hotel_rooms where room_number = %s"
    result = _execute_read_query(con, select_description, [room_number])
    connection_pool.putconn(con)
    return result[0][0]


def reserve(room_number, arrival_date, departure_date, name, phone, count):
    con = connection_pool.getconn()
    insert_reserve = "insert into reservations(room_number, date_of_arrival, date_of_departure," \
                     " client_name, client_phone_number, count_of_people) values" \
                     " (%s, %s,%s,%s,%s,%s)"
    params = [room_number, arrival_date, departure_date, name, phone, count]
    _execute_query(con, insert_reserve, params)
    connection_pool.putconn(con)


if __name__ == '__main__':
    vac = vacant_room('Стандарт', 4, '4.3.2020', '5.3.2020')
    print(vac)
    desc = description(1)
    print(desc)
