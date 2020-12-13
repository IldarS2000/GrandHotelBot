/*
 наиболее популярные комнаты
 */


create or replace function most_vacant(m_c int)
    returns table
            (
                room_n int,
                res_n bigint
            )
    language 'plpgsql'
as
$$
begin
    return query
        select room_number, count(*) count from reservations
        group by room_number
        order by count desc
    limit m_c;
end;
$$;


/*
 наименее популярные комнаты
 */

create or replace function less_vacant_room(m_c int)
    returns table
            (
                room_n int,
                res_n bigint
            )
    language 'plpgsql'
as
$$
begin
    return query
        select room_number, count(*) count from reservations
        group by room_number
        order by count
    limit m_c;
end;
$$;

/*
 последняя оканчивающаяся бронь
 */

create or replace function last_booked_room()
    returns table
            (
                id_      int,
    room_number_         int,
    date_of_arrival_     date ,
    date_of_departure_   date ,
    client_name_         varchar(30) ,
    client_phone_number_ varchar(15) ,
    count_of_people_     int
            )
    language 'plpgsql'
as
$$
begin
    return query
        select id,room_number ,date_of_arrival  ,date_of_departure ,client_name   ,client_phone_number ,count_of_people  from reservations
        order by date_of_departure desc
        limit 1;
end;
$$;


/*
 наиболее частые постояльцы
 */

create or replace function best_costumer(i int)
    returns table
            (
    name_  varchar(30),
    amount     bigint
            )
    language 'plpgsql'
as
$$
begin
    return query
        select client_name, count(*) count from reservations
        group by client_name
        order by count desc
        limit i;
end;
$$;

/*
 наиболее прибыльные комнаты
 */
create or replace function most_profitable_rooms(a date,b date,m_c int)
    returns table
            (
    room_num  int,
    cash    double precision
            )
    language 'plpgsql'

as
$$
begin
        return query
            with z1 as (select r.room_number, r.date_of_arrival, r.date_of_departure
                        from reservations r
                        where ((a <= date_of_arrival and date_of_arrival <= b) or
                               (a <= date_of_departure and date_of_departure <= b))),
                 z2 as (select z1.room_number,
                               sum(extract(day from age(date_of_departure, date_of_arrival)) +
                                   extract(month from age(date_of_departure, date_of_arrival) * 30) +
                                   extract(year from age(date_of_departure, date_of_arrival) * 365)) count,
                               hotel_rooms.price_per_day
                        from z1
                                 join hotel_rooms on hotel_rooms.room_number = z1.room_number
                        group by z1.room_number,hotel_rooms.price_per_day)
            select z2.room_number, z2.count*z2.price_per_day f from z2 order by f desc limit m_c;

end;
$$;

/*
 наименее прибыльные номера
 */
create or replace function least_profitable_rooms(a date,b date,m_c int)
    returns table
            (
    room_num  int,
    cash    double precision
            )
    language 'plpgsql'

as
$$
begin
        return query
            with z1 as (select r.room_number, r.date_of_arrival, r.date_of_departure
                        from reservations r
                        where ((a <= date_of_arrival and date_of_arrival <= b) or
                               (a <= date_of_departure and date_of_departure <= b))),
                 z2 as (select z1.room_number,
                               sum(extract(day from age(date_of_departure, date_of_arrival)) +
                                   extract(month from age(date_of_departure, date_of_arrival) * 30) +
                                   extract(year from age(date_of_departure, date_of_arrival) * 365)) count,
                               hotel_rooms.price_per_day
                        from z1
                                 join hotel_rooms on hotel_rooms.room_number = z1.room_number
                        group by z1.room_number,hotel_rooms.price_per_day)
            select z2.room_number, z2.count*z2.price_per_day f from z2 order by f limit m_c;

end;
$$;

/*
 наиболее надолгобронируемые комнаты
 */

create or replace function most_long_time_booking_rooms(a date,b date,m_c int)
    returns table
            (
    room_num  int,
    avarage_days    double precision
            )
    language 'plpgsql'

as
$$
begin
    return query
        with z1 as (select r.room_number, r.date_of_arrival, r.date_of_departure
                    from reservations r
                    where ((a <= date_of_arrival and date_of_arrival <= b) or
                           (a <= date_of_departure and date_of_departure <= b))),
             z2 as (select z1.room_number,
                           sum(extract(day from age(date_of_departure, date_of_arrival)) +
                               extract(month from age(date_of_departure, date_of_arrival) * 30) +
                               extract(year from age(date_of_departure, date_of_arrival) * 365)) sumday
                            ,
                           count(*) count
                    from z1
                    group by z1.room_number)
        select z2.room_number, z2.sumday / z2.count f
        from z2
        order by f desc
        limit m_c;


end;
$$;


/*
 наименее надолгобронируемые комнаты
 */


create or replace function least_long_time_booking_rooms(a date,b date,m_c int)
    returns table
            (
    room_num  int,
    avarage_days    double precision
            )
    language 'plpgsql'

as
$$
begin
    return query
        with z1 as (select r.room_number, r.date_of_arrival, r.date_of_departure
                    from reservations r
                    where ((a <= date_of_arrival and date_of_arrival <= b) or
                           (a <= date_of_departure and date_of_departure <= b))),
             z2 as (select z1.room_number,
                           sum(extract(day from age(date_of_departure, date_of_arrival)) +
                               extract(month from age(date_of_departure, date_of_arrival) * 30) +
                               extract(year from age(date_of_departure, date_of_arrival) * 365)) sumday
                            ,
                           count(*) count
                    from z1
                    group by z1.room_number)
        select z2.room_number, z2.sumday / z2.count f
        from z2
        order by f
        limit m_c;


end;
$$;


/*
 наименее заполненная комната
 */

create or replace function least_filled_rooms(m_c int)
    returns table
            (
    room_num  int,
    filled_prec  numeric
            )
    language 'plpgsql'

as
$$
begin
    return query
        with z1 as (select r.room_number, sum(r.count_of_people) sum_people, count(*) count, hotel_rooms.max_people
                    from reservations r join hotel_rooms on hotel_rooms.room_number = r.room_number
                    group by r.room_number, hotel_rooms.max_people)
        select z1.room_number,  z1.sum_people * 1.01 / 1.01 / z1.count / z1.max_people * 100 f
        from z1
        order by f
        limit m_c;


end;
$$;

/*
 наиболее заполненная комната
 */

create or replace function most_filled_rooms(m_c int)
    returns table
            (
    room_num  int,
    filled_prec  numeric
            )
    language 'plpgsql'

as
$$
begin
    return query
        with z1 as (select r.room_number, sum(r.count_of_people) sum_people, count(*) count, hotel_rooms.max_people
                    from reservations r join hotel_rooms on hotel_rooms.room_number = r.room_number
                    group by r.room_number, hotel_rooms.max_people)
        select z1.room_number,  z1.sum_people * 1.01 / 1.01 / z1.count / z1.max_people * 100 f
        from z1
        order by f desc
        limit m_c;


end;
$$;

/*
 самый нагруженный по броням месяц
 */
create or replace function most_F_month(m_c int)
    returns table
            (
    month  double precision,
    bookings    bigint
            )
    language 'plpgsql'

as
$$
begin
    return query
        select extract(month from date_of_arrival) s, count(*) count
        from reservations
        group by s
        order by count desc
        limit m_c;


end;
$$;

create or replace function least_booked_month(m_c int)
    returns table
            (
    month  double precision,
    bookings    bigint
            )
    language 'plpgsql'

as
$$
begin
    return query
        select extract(month from date_of_arrival) s, count(*) count
        from reservations
        group by s
        order by count
        limit m_c;


end;
$$;