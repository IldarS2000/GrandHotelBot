from aiogram import types
from bot import dp


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer('Здравствуйте вас приветствует бот для бронирования номеров отеля Grand Hotel!')
