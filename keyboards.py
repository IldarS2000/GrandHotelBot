from aiogram import types


def add_buttons_to_keyboard(keyboard, buttons):
    for button in buttons:
        keyboard.add(button)


# КЛАВИАТУРЫ ГЛАВНОГО МЕНЮ
main_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
book_room_button = ['Забронировать номер']
services_button = ['Ознакомиться с зоной отдыха']
feedback_button = ['Обратная связь']
menu_buttons = book_room_button + services_button + feedback_button
add_buttons_to_keyboard(main_menu_keyboard, menu_buttons)

# КЛАВИАТУРЫ БРОНИРОВАНИЯ НОМЕРА
type_of_rooms_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
type_of_rooms_buttons = ['Президентский', 'Люкс', 'Стандарт']
add_buttons_to_keyboard(type_of_rooms_keyboard, type_of_rooms_buttons)

book_room_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_to_choosing_room_button = ['Назад к выбору комнат']
book_room_buttons = book_room_button + back_to_choosing_room_button
add_buttons_to_keyboard(book_room_keyboard, book_room_buttons)

accept_data_button = ['Подтвердить данные']
change_data_button = ['Изменить данные']
accept_data_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
add_buttons_to_keyboard(accept_data_keyboard, accept_data_button + change_data_button)

# КЛАВИАТУРЫ ДОПОЛНИТЕЛЬНЫХ УСЛУГ
# КЛАВИАТУРЫ ДЛЯ ФИДБЕКА

# ОБЩИЕ КНОПКИ
back_to_main_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_to_main_menu_button = ['Главное меню']
add_buttons_to_keyboard(back_to_main_menu_keyboard, back_to_main_menu_button)

keyboard_with_back_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_button = ['Назад']
add_buttons_to_keyboard(keyboard_with_back_button, back_button)
