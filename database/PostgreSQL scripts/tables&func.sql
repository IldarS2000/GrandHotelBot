create table hotel_rooms
(
    room_number   int primary key,
    type          varchar(15) check ( type in ('Президентский', 'Люкс', 'Стандарт') ) not null,
    price_per_day int check ( price_per_day > 0 )                                     not null,
    max_people    int check ( max_people > 0 )                                        not null,
    count_of_beds int check ( 0 < count_of_beds and count_of_beds <= max_people )     not null,
    description   text                                                                not null
);

create table reservations
(
    id                  serial primary key,
    room_number         int references hotel_rooms (room_number),
    date_of_arrival     date                                               not null,
    date_of_departure   date check ( date_of_arrival < date_of_departure ) not null,
    client_name         varchar(30)                                        not null,
    client_phone_number varchar(15)                                        not null,
    count_of_people     int check ( count_of_people > 0 )                  not null
);

create table feedback
(
    id      serial primary key,
    rating  int check ( rating > 0 and rating <= 5 ) not null,
    comment text                                     not null
);


create or replace function vacant_room(type_of_room varchar(15), count int, arrival_date date, departure_date date)
    returns table
            (
                room_number   int,
                price_per_day int,
                count_of_beds int
            )
    language plpgsql
as
$$
begin
    return query
        select distinct h.room_number, h.price_per_day, h.count_of_beds
        from hotel_rooms h
                 left join reservations r on h.room_number = r.room_number
        where h.type = type_of_room
          and count <= h.max_people
          and h.room_number not in (select r2.room_number
                                    from reservations r2
                                    where ((r2.date_of_arrival <= arrival_date and arrival_date <= r2.date_of_departure)
                                        or (r2.date_of_arrival <= departure_date and
                                            departure_date <= r2.date_of_departure))
                                       or (arrival_date <= r2.date_of_arrival and
                                           r2.date_of_departure <= departure_date))
        order by h.room_number;
end
$$;