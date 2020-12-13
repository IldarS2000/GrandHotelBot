from aiogram.dispatcher.filters.state import State, StatesGroup


class MainForm(StatesGroup):
    menu = State()


class RoomsForm(StatesGroup):
    menu = State()
    getting_arrival_date = State()
    getting_departure_date = State()
    counting_humans = State()
    accepting_data1 = State()
    choosing_type_of_room = State()
    choosing_specific_room = State()
    booking_specific_room = State()

    getting_name = State()
    getting_phone_number = State()
    accepting_data2 = State()


class ServicesForm(StatesGroup):
    menu = State()
    checking_service = State()


class FeedbackForm(StatesGroup):
    menu = State()
    getting_feedback = State()


main_menu = [RoomsForm.getting_arrival_date, ServicesForm.menu, FeedbackForm.menu]
