from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.ru_lexicon import keyboard_lexicon


menu_keyboard_builder = ReplyKeyboardBuilder()
menu_buttons = [KeyboardButton(text=keyboard_lexicon['menu'][i]) for i in range(len(keyboard_lexicon['menu']))]
menu_keyboard_builder.add(*menu_buttons)
menu_keyboard = menu_keyboard_builder.as_markup(one_time_keyboard=True)


