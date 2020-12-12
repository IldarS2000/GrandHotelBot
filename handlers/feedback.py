from aiogram import types

from bot import dp
from states import MainForm, FeedbackForm
from keyboards import back_to_main_menu_keyboard


@dp.message_handler(lambda message: message.text in 'Обратная связь',
                    state=MainForm.menu,
                    content_types=types.ContentTypes.TEXT)
async def process_feedback(message: types.Message):
    await FeedbackForm.menu.set()
    await message.answer('напишите отзыв или предложение мы обязательно его рассмотрим',
                         reply_markup=back_to_main_menu_keyboard)


@dp.message_handler(state=FeedbackForm.menu, content_types=types.ContentTypes.TEXT)
async def load_feedback(message: types.Message):
    await message.reply('спасибо!')
