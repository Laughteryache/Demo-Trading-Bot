from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import keyboard_lexicon

#MENU_KEYBOARD
menu_keyboard_builder = ReplyKeyboardBuilder()
menu_buttons = [KeyboardButton(text=i) for i in keyboard_lexicon['menu'].values()]
menu_keyboard_builder.add(*menu_buttons)
menu_keyboard = menu_keyboard_builder.as_markup(one_time_keyboard=True, resize_keyboard=True)

#FUNC_SEND_LIST_INLINE_KEYBOARD
button_1 = InlineKeyboardButton(
    text='BTC/USDT',
    callback_data='0'
)
button_2 = InlineKeyboardButton(
    text='ETH/USDT',
    callback_data='1'
)
button_3 = InlineKeyboardButton(
    text='SOL/USDT',
    callback_data='2'
)
courses_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1],
                                                         [button_2],
                                                         [button_3]])