from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.ru_lexicon import keyboard_lexicon


menu_keyboard_builder = ReplyKeyboardBuilder()
menu_buttons = [KeyboardButton(text=i, callback_data=j) for i, j in keyboard_lexicon['menu'].items()]
menu_keyboard_builder.add(*menu_buttons)
menu_keyboard = menu_keyboard_builder.as_markup(one_time_keyboard=True, resize_keyboard=True)


