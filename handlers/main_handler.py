from aiogram import types

from bot import dp
from states import MainForm, main_menu
from keyboards import main_menu_keyboard


@dp.message_handler(state='*', commands='start')
async def cmd_start(message: types.Message):
    await message.answer('Здравствуйте, вас приветствует бот отеля Grand Hotel!')
    await MainForm.menu.set()
    await message.answer('Выберите дальнейшее действие',
                         reply_markup=main_menu_keyboard)


@dp.message_handler(lambda message: message.text == 'Главное меню', state=main_menu,
                    content_types=types.ContentTypes.TEXT)
async def process_menu(message: types.Message):
    await MainForm.menu.set()
    await message.answer('Выберите номер или ознакомьтесь с нашей зоной отдыха',
                         reply_markup=main_menu_keyboard)


@dp.message_handler(state='*', commands='help')
async def cmd_help(message: types.Message):
    await message.answer('для возврата в главное меню нажмите: /start\n'
                         'формат записи дат: "DD.MM.YYYY" без кавычек\n'
                         'в разделе "обратная связь" вы можете оставить отзыв\n'
                         'по всем оставшимся вопросам звоните по номеру: 467382')
