from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import dp
from states import MainForm, FeedbackForm
from keyboards import feedback_keyboard, feedback_buttons


@dp.message_handler(lambda message: message.text in 'Обратная связь',
                    state=MainForm.menu,
                    content_types=types.ContentTypes.TEXT)
async def process_feedback(message: types.Message):
    await FeedbackForm.menu.set()
    await message.answer('напишите отзыв или предложение мы обязательно его рассмотрим',
                         reply_markup=feedback_keyboard)


@dp.message_handler(state=FeedbackForm.menu, content_types=types.ContentTypes.TEXT)
async def load_feedback(message: types.Message):
    await message.reply('спасибо!')
