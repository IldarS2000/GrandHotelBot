from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import dp
from states import MainForm, main_menu
from keyboards import main_menu_keyboard, menu_buttons


@dp.message_handler(state='*', commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer('Здравствуйте вас приветствует бот отеля Grand Hotel!')
    await MainForm.menu.set()
    await message.answer('выберите номер или ознакомьтесь с нашей зоной отдыха',
                         reply_markup=main_menu_keyboard)


@dp.message_handler(lambda message: message.text == 'Главное меню', state=main_menu,
                    content_types=types.ContentTypes.TEXT)
async def process_menu(message: types.Message, state: FSMContext):
    await MainForm.menu.set()
    await message.answer('выберите номер или ознакомьтесь с нашей зоной отдыха',
                         reply_markup=main_menu_keyboard)


@dp.message_handler(lambda message: message.text not in menu_buttons, state=MainForm.menu)
async def process_menu_invalid(message: types.Message):
    await message.reply('ошибка ввода, нажмите одну из кнопок')
