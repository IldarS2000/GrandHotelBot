from aiogram import types

from bot import dp
from states import MainForm, ServicesForm
from keyboards import back_to_main_menu_keyboard, keyboard_with_back_button, services_button, back_button


@dp.message_handler(lambda message: message.text in services_button + back_button,
                    state=[MainForm.menu, ServicesForm.checking_service],
                    content_types=types.ContentTypes.TEXT)
async def process_services_button(message: types.Message):
    await ServicesForm.menu.set()
    await message.answer('Введите порядковое число услуги, которую хотите рассмотреть, например "1"\n'
                         '1. баня\n'
                         '2. ресторан\n'
                         '3. бильярд\n', reply_markup=back_to_main_menu_keyboard)


def filter_service_number(message: types.Message):
    if message.text.isdigit():
        if 1 <= int(message.text) <= 3:
            return True
    return False


@dp.message_handler(lambda message: not filter_service_number(message), state=ServicesForm.menu)
async def book_room_invalid(message: types.Message):
    await message.reply('введен не существующий номер, попробуйте снова')


@dp.message_handler(filter_service_number, state=ServicesForm.menu)
async def book_room(message: types.Message):
    await ServicesForm.checking_service.set()
    await message.reply('отличный выбор!', reply_markup=keyboard_with_back_button)
