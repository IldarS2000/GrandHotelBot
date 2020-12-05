from aiogram import types
import re


def add_buttons_to_keyboard(keyboard, buttons):
    for button in buttons:
        keyboard.add(button)


main_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu_buttons = ['Выбрать номер', 'Ознакомиться с зоной отдыха', 'Обратная связь']
add_buttons_to_keyboard(main_menu_keyboard, menu_buttons)

rooms_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
rooms_buttons = ['Главное меню']
add_buttons_to_keyboard(rooms_keyboard, rooms_buttons)

services_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
services_buttons = ['Главное меню']
add_buttons_to_keyboard(services_keyboard, services_buttons)

keyboard_with_back_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_with_back_button.add('Назад')

feedback_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
feedback_buttons = ['Главное меню']
add_buttons_to_keyboard(feedback_keyboard, feedback_buttons)
