from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import dp
from states import MainForm, RoomsForm
from keyboards import rooms_keyboard, rooms_buttons, keyboard_with_back_button


@dp.message_handler(lambda message: message.text in ['Выбрать номер', 'Назад'],
                    state=[MainForm.menu, RoomsForm.booking_room],
                    content_types=types.ContentTypes.TEXT)
async def process_booking_button(message: types.Message):
    await RoomsForm.menu.set()
    await message.answer('Введите порядковое число номера, который хотите рассмотреть, например "1"\n'
                         '1. люкс\n'
                         '2. средний класс\n'
                         '3. эконом класс\n', reply_markup=rooms_keyboard)


def filter_room_number(message: types.Message):
    if message.text.isdigit():
        if 1 <= int(message.text) <= 3:
            return True
    return False


@dp.message_handler(lambda message: not filter_room_number(message), state=RoomsForm.menu)
async def book_room_invalid(message: types.Message):
    await message.reply('введен не существующий номер, попробуйте снова')


@dp.message_handler(filter_room_number, state=RoomsForm.menu)
async def book_room(message: types.Message):
    await RoomsForm.booking_room.set()
    await message.reply('отличный выбор!', reply_markup=keyboard_with_back_button)
