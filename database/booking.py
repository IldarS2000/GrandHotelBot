import psycopg2
from psycopg2 import OperationalError


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host,
                                      port=db_port, )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def vacant_room(type, count, arrival_date, departure_date):
    con = create_connection('hotel', 'postgres', 'kekwmek1', 'localhost', '5432')
    select_vacant = "select * from vacant_room('" + type + "'," + \
                    str(count) + ",'" + arrival_date + "','" + departure_date + "')"

    result = execute_read_query(con, select_vacant)
    return result


def desription(room_number):
    con = create_connection('hotel', 'postgres', 'kekwmek1', 'localhost', '5432')
    select_description = "select description from hotel_rooms"

    result = execute_read_query(con, select_description)

    return result


def reserve(room_number, arrival_date, departure_date, name, phone, count):
    con = create_connection('hotel', 'postgres', 'kekwmek1', 'localhost', '5432')
    insert_reserve = """insert into reservations(room_number, date_of_arrival, date_of_departure, client_name,
     client_phone_number,count_of_people) values (""" + str(room_number) + ",'" + arrival_date + "','" \
                     + departure_date + "','" + name + "','" + phone + "'," + str(count) + ")"
    execute_query(con,insert_reserve)

if __name__ == '__main__':
    vac = vacant_room('Президентский', 1, '3.4.2020', '30.5.2020')
    print(vac)
    desc = desription(1)
    print(desc)
    reserve(1,'3.4.2020', '30.5.2020', 'Serega', '89993331122', 1)


