from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import dp
from database import queries
from states import MainForm, FeedbackForm
from keyboards import back_to_main_menu_keyboard, feedback_button, estimations_keyboard


@dp.message_handler(lambda message: message.text in feedback_button,
                    state=MainForm.menu,
                    content_types=types.ContentTypes.TEXT)
async def process_feedback(message: types.Message):
    await FeedbackForm.menu.set()
    await message.answer('оцените нас, мы будем очень рады!\n'
                         'поставьте оценку от 1 до 5',
                         reply_markup=estimations_keyboard)


def filter_estimation(message: types.Message):
    if message.text.isdigit():
        if 1 <= int(message.text) <= 5:
            return True
    return False


@dp.message_handler(lambda message: not filter_estimation(message), state=FeedbackForm.menu)
async def choose_estimation_invalid(message: types.Message):
    await message.reply('введена некорректная оценка, попробуйте снова')


@dp.message_handler(filter_estimation, state=FeedbackForm.menu, content_types=types.ContentTypes.TEXT)
async def choose_estimation(message: types.Message, state: FSMContext):
    await FeedbackForm.getting_feedback.set()
    await state.update_data(estimation=message.text)
    await message.answer('теперь напишите о нас отзыв :)', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=FeedbackForm.getting_feedback, content_types=types.ContentTypes.TEXT)
async def write_feedback(message: types.Message, state: FSMContext):
    await FeedbackForm.menu.set()
    user_data = await state.get_data()
    estimation = user_data['estimation']
    feedback = message.text

    queries.upload_feedback(estimation, feedback)

    await message.answer('спасибо!\n'
                         'теперь вы можете перейти в главное меню', reply_markup=back_to_main_menu_keyboard)
