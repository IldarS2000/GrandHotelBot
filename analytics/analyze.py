from psycopg2 import OperationalError
from psycopg2 import sql, pool
from database.config import *

connection_pool = pool.SimpleConnectionPool(10, 50,
                                            database=database,
                                            user=user,
                                            password=password,
                                            host=host,
                                            port=port)



def _execute_read_query(connection, query, params):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def most_vacant(lim):
    con = connection_pool.getconn()
    select_most_vacant = "select * from most_vacant(%s)"
    params = [lim]
    result = _execute_read_query(con, select_most_vacant, params)
    connection_pool.putconn(con)
    return result

def less_vacant_room(lim):
    con = connection_pool.getconn()
    select_least_vacant = "select * from less_vacant_room(%s)"
    params = [lim]
    result = _execute_read_query(con, select_least_vacant, params)
    connection_pool.putconn(con)
    return result

def last_booked_room():
    con = connection_pool.getconn()
    select_last_booked_room = "select * from last_booked_room()"
    params = []
    result = _execute_read_query(con, select_last_booked_room, params)
    connection_pool.putconn(con)
    return result

def best_costumer(lim):
    con = connection_pool.getconn()
    select_least_vacant = "select * from best_costumer(%s)"
    params = [lim]
    result = _execute_read_query(con, select_least_vacant, params)
    connection_pool.putconn(con)
    return result

def most_profitable_rooms(Adata,Bdata,lim):
    con = connection_pool.getconn()
    select_least_vacant = "select * from most_profitable_rooms(%s,%s,%s)"
    params = [Adata,Bdata,lim]
    result = _execute_read_query(con, select_least_vacant, params)
    connection_pool.putconn(con)
    return result

def least_profitable_rooms(Adata,Bdata,lim):
    con = connection_pool.getconn()
    select_least_vacant = "select * from least_profitable_rooms(%s,%s,%s)"
    params = [Adata,Bdata,lim]
    result = _execute_read_query(con, select_least_vacant, params)
    connection_pool.putconn(con)
    return result

def most_long_time_booking_rooms(Adata,Bdata,lim):
    con = connection_pool.getconn()
    select_least_vacant = "select * from most_long_time_booking_rooms(%s,%s,%s)"
    params = [Adata,Bdata,lim]
    result = _execute_read_query(con, select_least_vacant, params)
    connection_pool.putconn(con)
    return result

def least_long_time_booking_rooms(Adata,Bdata,lim):
    con = connection_pool.getconn()
    select_least_vacant = "select * from least_long_time_booking_rooms(%s,%s,%s)"
    params = [Adata,Bdata,lim]
    result = _execute_read_query(con, select_least_vacant, params)
    connection_pool.putconn(con)
    return result

def least_filled_rooms(lim):
    con = connection_pool.getconn()
    select_least_vacant = "select * from least_filled_rooms(%s)"
    params = [lim]
    result = _execute_read_query(con, select_least_vacant, params)
    connection_pool.putconn(con)
    return result

def most_filled_rooms(lim):
    con = connection_pool.getconn()
    select_least_vacant = "select * from most_filled_rooms(%s)"
    params = [lim]
    result = _execute_read_query(con, select_least_vacant, params)
    connection_pool.putconn(con)
    return result

def most_booked_month(lim):
    con = connection_pool.getconn()
    select_least_vacant = "select * from most_booked_month(%s)"
    params = [lim]
    result = _execute_read_query(con, select_least_vacant, params)
    connection_pool.putconn(con)
    return result

def least_booked_month(lim):
    con = connection_pool.getconn()
    select_least_vacant = "select * from least_booked_month(%s)"
    params = [lim]
    result = _execute_read_query(con, select_least_vacant, params)
    connection_pool.putconn(con)
    return result

if __name__ == '__main__':
    vac = least_booked_month(5)
    print(vac)
