import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from database import queries
from bot import dp, bot
from states import MainForm, RoomsForm, main_menu
from keyboards import keyboard_with_back_button, back_button, \
    type_of_rooms_keyboard, type_of_rooms_buttons, \
    book_room_keyboard, \
    accept_data_keyboard, accept_data_button, change_data_button, \
    back_to_main_menu_keyboard, \
    back_to_choosing_room_button, \
    book_room_button


def is_date(date):
    return re.match(r'^(3[01]|[12][0-9]|0?[1-9])\.(1[0-2]|0?[1-9])\.(?:[0-9]{2})?[0-9]{2}$', date)


def is_phone_humber(number):
    return re.match(r'^\+?\d+$', number)


@dp.message_handler(lambda message: message.text in book_room_button + change_data_button,
                    state=[MainForm.menu, RoomsForm.accepting_data1],
                    content_types=types.ContentTypes.TEXT)
async def choose_arrival_date(message: types.Message):
    await RoomsForm.getting_arrival_date.set()
    await message.answer(
        'Введите дату заезда в следующем формате: "DD.MM.YYYY" без кавычек, пример: "25.05.2020"',
        reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: is_date(message.text),
                    state=RoomsForm.getting_arrival_date,
                    content_types=types.ContentTypes.TEXT)
async def choose_date_of_departure(message: types.Message, state: FSMContext):
    await RoomsForm.getting_departure_date.set()
    await state.update_data(arrival_date=message.text)
    await message.answer('Введите дату отъезда в следующем формате: "DD.MM.YYYY" без кавычек, пример: "25.05.2020"')


@dp.message_handler(lambda message: not is_date(message.text),
                    state=[RoomsForm.getting_arrival_date, RoomsForm.getting_departure_date])
async def choose_date_invalid(message: types.Message):
    await message.reply('введен не корректный формат даты')


@dp.message_handler(lambda message: is_date(message.text),
                    state=RoomsForm.getting_departure_date,
                    content_types=types.ContentTypes.TEXT)
async def choose_count_of_humans(message: types.Message, state: FSMContext):
    await RoomsForm.counting_humans.set()
    await state.update_data(departure_date=message.text)
    await message.answer('Введите количество людей')


@dp.message_handler(lambda message: message.text.isdigit(),
                    state=RoomsForm.counting_humans,
                    content_types=types.ContentTypes.TEXT)
async def accept_data(message: types.Message, state: FSMContext):
    await RoomsForm.accepting_data1.set()
    await state.update_data(humans_count=message.text)

    user_data = await state.get_data()
    await message.answer(f'введенные данные\n'
                         f'   дата заезда: {user_data["arrival_date"]}\n'
                         f'   дата выезда: {user_data["departure_date"]}\n'
                         f'   количество человек: {user_data["humans_count"]}\n'
                         f'подтвердите введенные данные или измените их',
                         reply_markup=accept_data_keyboard)


@dp.message_handler(lambda message: message.text in back_button + accept_data_button + back_to_choosing_room_button,
                    state=[RoomsForm.accepting_data1, RoomsForm.choosing_specific_room,
                           RoomsForm.booking_specific_room],
                    content_types=types.ContentTypes.TEXT)
async def choose_type_of_room(message: types.Message):
    await RoomsForm.choosing_type_of_room.set()
    await message.answer('Выберите тип номера', reply_markup=type_of_rooms_keyboard)


@dp.message_handler(lambda message: message.text in type_of_rooms_buttons,
                    state=RoomsForm.choosing_type_of_room,
                    content_types=types.ContentTypes.TEXT)
async def choose_specific_room(message: types.Message, state: FSMContext):
    await RoomsForm.choosing_specific_room.set()

    await state.update_data(room_type=message.text)

    user_data = await state.get_data()
    room_type = user_data['room_type']
    count = user_data['humans_count']
    arrival_date = user_data['arrival_date']
    departure_date = user_data['departure_date']

    rooms = queries.vacant_room(room_type, count, arrival_date, departure_date)

    if not rooms:
        await message.answer('К сожалению нет подходящих комнат', reply_markup=keyboard_with_back_button)
    else:
        answer = ''
        for room in rooms:
            answer += f'{room[0]}, цена: {room[1]}, количество кроватей: {room[2]}\n'
        await message.answer(answer)
        await message.answer('Выберите номер комнаты', reply_markup=keyboard_with_back_button)


@dp.message_handler(lambda message: message.text.isdigit(),
                    state=RoomsForm.choosing_specific_room,
                    content_types=types.ContentTypes.TEXT)
async def book_room(message: types.Message, state: FSMContext):
    await RoomsForm.booking_specific_room.set()
    await state.update_data(booked_room=message.text)

    user_data = await state.get_data()
    room_number = user_data['booked_room']
    description = queries.description(room_number)

    room_type = user_data['room_type']

    rooms = {'Президентский': 'prezident', 'Люкс': 'lux', 'Стандарт': 'standart'}
    img = open(f'images/rooms/{rooms[room_type]}/photo.jpg', 'rb')

    await message.answer(description)
    await bot.send_photo(message.chat.id, img)
    await message.answer('Можете забронировать номер или перейти обратно к списку номеров',
                         reply_markup=book_room_keyboard)


@dp.message_handler(lambda message: message.text in book_room_button + change_data_button,
                    state=[RoomsForm.booking_specific_room, RoomsForm.accepting_data2],
                    content_types=types.ContentTypes.TEXT)
async def get_name(message: types.Message):
    await RoomsForm.getting_name.set()
    await message.answer('Введите ваше имя',
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=RoomsForm.getting_name,
                    content_types=types.ContentTypes.TEXT)
async def get_phone_number(message: types.Message, state: FSMContext):
    await RoomsForm.getting_phone_number.set()
    await state.update_data(name=message.text)
    await message.answer(
        'Введите мобильный номер по которому оператор сможет с вами связаться и подтвердить бронирование')


@dp.message_handler(lambda message: not is_phone_humber(message.text),
                    state=RoomsForm.getting_phone_number,
                    content_types=types.ContentTypes.TEXT)
async def get_phone_number_invalid(message: types.Message):
    await message.reply('некорректный формат номера телефона')


@dp.message_handler(lambda message: is_phone_humber(message.text),
                    state=RoomsForm.getting_phone_number,
                    content_types=types.ContentTypes.TEXT)
async def accept_data(message: types.Message, state: FSMContext):
    await RoomsForm.accepting_data2.set()
    await state.update_data(phone_number=message.text)

    user_data = await state.get_data()
    await message.answer(f'введенные данные\n'
                         f'   имя: {user_data["name"]}\n'
                         f'   номер телефона: {user_data["phone_number"]}\n'
                         f'подтвердите введенные данные или измените их',
                         reply_markup=accept_data_keyboard)


@dp.message_handler(lambda message: message.text in accept_data_button,
                    state=RoomsForm.accepting_data2,
                    content_types=types.ContentTypes.TEXT)
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await main_menu[0].set()

    user_data = await state.get_data()
    room_number = user_data['booked_room']
    arrival_date = user_data['arrival_date']
    departure_date = user_data['departure_date']
    name = user_data['name']
    phone = user_data['phone_number']
    count = user_data['humans_count']

    queries.reserve(room_number, arrival_date, departure_date, name, phone, count)

    await message.answer('Номер зарезирвирован, сейчас с вами свяжется наш агент\n'
                         'пока вы можете перейти в главное меню',
                         reply_markup=back_to_main_menu_keyboard)
