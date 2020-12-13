from psycopg2 import OperationalError
from psycopg2 import sql, pool
from database.config import *
from prettytable import PrettyTable
import os

connection_pool = pool.SimpleConnectionPool(10, 50,
                                            database=database,
                                            user=user,
                                            password=password,
                                            host=host,
                                            port=port)


def output(th, td):
    columns = len(th)  # Подсчитаем кол-во столбцов на будущее.

    table = PrettyTable(th)  # Определяем таблицу.

    # Cкопируем список td, на случай если он будет использоваться в коде дальше.
    td_data = td[:]
    # Входим в цикл который заполняет нашу таблицу.
    # Цикл будет выполняться до тех пор пока у нас не кончатся данные
    # для заполнения строк таблицы (список td_data).
    while td_data:
        # Используя срез добавляем первые пять элементов в строку.
        # (columns = 5).
        table.add_row(td_data[:columns])
        # Используя срез переопределяем td_data так, чтобы он
        # больше не содержал первых 5 элементов.
        td_data = td_data[columns:]

    print(table)  # Печатаем таблицу


def _execute_read_query(connection, query, params):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def last_booked_room():
    con = connection_pool.getconn()
    select_last_booked_room = "select * from last_booked_room()"
    params = []
    result = _execute_read_query(con, select_last_booked_room, params)
    connection_pool.putconn(con)
    return result


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


def best_costumer(lim):
    con = connection_pool.getconn()
    select_least_vacant = "select * from best_costumer(%s)"
    params = [lim]
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


def most_profitable_rooms(Adata, Bdata, lim):
    con = connection_pool.getconn()
    select_least_vacant = "select * from most_profitable_rooms(%s,%s,%s)"
    params = [Adata, Bdata, lim]
    result = _execute_read_query(con, select_least_vacant, params)
    connection_pool.putconn(con)
    return result


def least_profitable_rooms(Adata, Bdata, lim):
    con = connection_pool.getconn()
    select_least_vacant = "select * from least_profitable_rooms(%s,%s,%s)"
    params = [Adata, Bdata, lim]
    result = _execute_read_query(con, select_least_vacant, params)
    connection_pool.putconn(con)
    return result


def most_long_time_booking_rooms(Adata, Bdata, lim):
    con = connection_pool.getconn()
    select_least_vacant = "select * from most_long_time_booking_rooms(%s,%s,%s)"
    params = [Adata, Bdata, lim]
    result = _execute_read_query(con, select_least_vacant, params)
    connection_pool.putconn(con)
    return result


def least_long_time_booking_rooms(Adata, Bdata, lim):
    con = connection_pool.getconn()
    select_least_vacant = "select * from least_long_time_booking_rooms(%s,%s,%s)"
    params = [Adata, Bdata, lim]
    result = _execute_read_query(con, select_least_vacant, params)
    connection_pool.putconn(con)
    return result


def feedback():
    con = connection_pool.getconn()
    select_feedback = "select * from feedback"
    params = []
    result = _execute_read_query(con, select_feedback, params)
    connection_pool.putconn(con)
    return result


def to_list(var):
    r = list()
    for i in var:
        for j in i:
            r.append(j)
    return r


def f2_3(td):
    th = ['Номер Комнаты', 'Количество броней']
    output(th, td)


def f4(td):
    th = ['Имя', 'Количество броней']
    output(th, td)


def f5_6(td):
    th = ['Номер комнаты', 'Процент заполнения']
    output(th, td)


def f7_8(td):
    th = ['Номер месяца', 'Количество заказов']
    output(th, td)


def onepar(f, p):
    ex = {
        2: most_vacant,
        3: less_vacant_room,
        4: best_costumer,
        5: least_filled_rooms,
        6: most_filled_rooms,
        7: most_booked_month,
        8: least_booked_month
    }
    var = ex[f](p)
    td = to_list(var)
    ex1 = {
        2: f2_3,
        3: f2_3,
        4: f4,
        5: f5_6,
        6: f5_6,
        7: f7_8,
        8: f7_8
    }
    q = ex1[f](td)


def f9_10(td):
    th = ['Номер комнаты', 'Прибыль с комнаты']
    output(th, td)


def f11_12(td):
    th = ['Номер комнаты', 'Дней брони в среднем']
    output(th, td)


def threepar(f, p3, p1='01.01.2017', p2='12.12.2020'):
    ex = {
        9: most_profitable_rooms,
        10: least_profitable_rooms,
        11: most_long_time_booking_rooms,
        12: least_long_time_booking_rooms
    }
    var = ex[f](p1, p2, p3)
    td = to_list(var)
    ex1 = {
        9: f9_10,
        10: f9_10,
        11: f11_12,
        12: f11_12,
    }
    q = ex1[f](td)


def statistics():
    kk = 1
    while kk == 1:
        print(' 1. Вывести самую позднюю бронь\n',
              '2. Вывести комнаты, пользующиеся наибольшим спросом\n',
              '3. Вывести комнаты, пользующиеся наименьшим спросом\n',
              '4. Вывести наиболее частых покупателей\n',
              '5. Вывести наименее наполняемые комнаты\n',
              '6. Вывести наиболее наполняемые комнаты\n',
              '7. Вывести месяцы с наибольшим числом бронирований\n',
              '8. Вывести месяцы с наименьшим числом бронирований\n',
              '9. Вывести наиболее доходные комнаты\n',
              '10. Вывести наименее доходные комнаты\n',
              '11. Вывести номера, бронируемые на самое длительное время\n',
              '12. Вывести номера, бронируемые на самое короткое время\n',
              '13. Выгрузить отзывы\n',
              '14. Закончить работу')

        b = 1
        fun = int()
        while b == 1:
            print('Введите цифру желаемой операции: ', end='')
            fun = int(input())
            if 0 < fun < 15:
                b = 4
            else:
                print("Введено некорректное число")

        if fun == 1:
            var = last_booked_room()
            # td = list(var[0][0],var[0][1],var[0][2],var[0][3],var[0][4],var[0][5],var[0][6])
            td = list(var[0])
            th = ['ID', 'Номер комнаты', 'Дата заезда', 'Дата выезда', 'Имя клиента', 'Номер телефона',
                  'Количество постояльцев']
            output(th, td)

        elif fun == 13:
            var = feedback()
            th = ['id', 'Рейтинг', 'Комментарий']
            td = to_list(var)
            output(th, td)

        elif 1 < fun < 13:
            print('Введите желаемое количество строчек в выводе: ', end='')
            p3 = int(input())
            if fun < 9:
                onepar(fun, p3)
            else:
                b = 0
                while b == 0:
                    print('Введите дату начала анализа в формате дд.мм.гггг: ', end='')
                    p1 = input()
                    print('Введите дату конца анализа в формате дд.мм.гггг: ', end='')
                    p2 = input()
                    if len(p1) > 0 and len(p2) > 0:
                        b = 1
                    else:
                        print("Введено некорректное значение")

                threepar(fun, p3, p1, p2)
        elif fun == 14:
            kk = 2
        print('Введите любой символ для продолжения...', end='')
        input()


if __name__ == '__main__':
    statistics()
