from aiogram.dispatcher.filters.state import State, StatesGroup


class MainForm(StatesGroup):
    menu = State()


class RoomsForm(StatesGroup):
    menu = State()
    booking_room = State()


class ServicesForm(StatesGroup):
    menu = State()
    checking_service = State()


class FeedbackForm(StatesGroup):
    menu = State()


main_menu = [RoomsForm.menu, ServicesForm.menu, FeedbackForm.menu]
