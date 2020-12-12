from aiogram import types
from aiogram.dispatcher import FSMContext
import re

from bot import dp
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


@dp.message_handler(lambda message: message.text in book_room_button + change_data_button,
                    state=[MainForm.menu, RoomsForm.accepting_data1],
                    content_types=types.ContentTypes.TEXT)
async def choose_arrival_date(message: types.Message):
    await RoomsForm.getting_arrival_date.set()
    await message.answer('Введите дату заезда как в следующем примере: "25.05.20"',
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: is_date(message.text),
                    state=RoomsForm.getting_arrival_date,
                    content_types=types.ContentTypes.TEXT)
async def choose_date_of_departure(message: types.Message, state: FSMContext):
    await RoomsForm.getting_departure_date.set()
    await state.update_data(arrival_date=message.text)
    await message.answer('Введите дату отъезда как в следующем примере: "03.06.20"')


@dp.message_handler(lambda message: is_date(message.text),
                    state=RoomsForm.getting_departure_date,
                    content_types=types.ContentTypes.TEXT)
async def choose_count_of_humans(message: types.Message, state: FSMContext):
    await RoomsForm.counting_humans.set()
    await state.update_data(departure_date=message.text)
    await message.answer('Введите сколько человек заедет в номер')


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


@dp.message_handler(lambda message: message.text in back_button + accept_data_button,
                    state=[RoomsForm.accepting_data1, RoomsForm.choosing_specific_room],
                    content_types=types.ContentTypes.TEXT)
async def choose_type_of_room(message: types.Message):
    await RoomsForm.choosing_type_of_room.set()
    await message.answer('Выберите тип номера', reply_markup=type_of_rooms_keyboard)


@dp.message_handler(lambda message: message.text in type_of_rooms_buttons + back_to_choosing_room_button,
                    state=[RoomsForm.choosing_type_of_room, RoomsForm.booking_specific_room],
                    content_types=types.ContentTypes.TEXT)
async def choose_specific_room(message: types.Message, state: FSMContext):
    await RoomsForm.choosing_specific_room.set()
    await state.update_data(room_type=message.text)
    await message.answer('Выберите комнату по её номеру', reply_markup=keyboard_with_back_button)


@dp.message_handler(lambda message: message.text.isdigit(),
                    state=RoomsForm.choosing_specific_room,
                    content_types=types.ContentTypes.TEXT)
async def book_room(message: types.Message, state: FSMContext):
    await RoomsForm.booking_specific_room.set()
    await state.update_data(booked_room=message.text)
    await message.answer('Можете забронировать номер, или перейти обратно к списку номеров',
                         reply_markup=book_room_keyboard)


@dp.message_handler(lambda message: message.text in book_room_button + change_data_button,
                    state=[RoomsForm.booking_specific_room, RoomsForm.accepting_data2],
                    content_types=types.ContentTypes.TEXT)
async def get_name(message: types.Message):
    await RoomsForm.getting_name.set()
    await message.answer('Введите имя по которому можно к вам обращаться',
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=RoomsForm.getting_name,
                    content_types=types.ContentTypes.TEXT)
async def get_phone_number(message: types.Message, state: FSMContext):
    await RoomsForm.getting_phone_number.set()
    await state.update_data(name=message.text)
    await message.answer(
        'Введите мобильный номер по которому оператор сможет с вами связаться и подтвердить бронирование')


@dp.message_handler(state=RoomsForm.getting_phone_number,
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
async def back_to_main_menu(message: types.Message):
    await main_menu[0].set()
    await message.answer('Номер зарезирвирован, сейчас с вами свяжется наш агент\n'
                         'пока вы можете перейти в главное меню',
                         reply_markup=back_to_main_menu_keyboard)

# def filter_room_number(message: types.Message):

#     if message.text.isdigit():
#         if 1 <= int(message.text) <= 3:
#             return True
#     return False
#
#
# @dp.message_handler(lambda message: not filter_room_number(message), state=RoomsForm.menu)
# async def book_room_invalid(message: types.Message):
#     await message.reply('введен не существующий номер, попробуйте снова')
#
#
# @dp.message_handler(filter_room_number, state=RoomsForm.menu)
# async def book_room(message: types.Message):
#     await RoomsForm.booking_room.set()
#     await message.reply('отличный выбор!', reply_markup=keyboard_with_back_button)
