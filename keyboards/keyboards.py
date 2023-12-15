from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from lexicon.lexicon import keyboard_lexicon, lexicon_currency

#MENU_KEYBOARD
menu_keyboard_builder = ReplyKeyboardBuilder()
menu_buttons = [KeyboardButton(text=i) for i in keyboard_lexicon['menu'].values()]
menu_keyboard_builder.add(*menu_buttons)
menu_keyboard = menu_keyboard_builder.as_markup(one_time_keyboard=True, resize_keyboard=True)


def pagination_keyboard(number: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    button_1 = InlineKeyboardButton(
        text=f'{lexicon_currency[number*3]}',
        callback_data=str(number*3)
    )
    button_2 = InlineKeyboardButton(
        text=f'{lexicon_currency[number*3+1]}',
        callback_data=str(number*3+1)
    )
    button_3 = InlineKeyboardButton(
        text=f'{lexicon_currency[number*3+2]}',
        callback_data=str(number*3+2)
    )
    forward = InlineKeyboardButton(
        text='>>',
        callback_data='forward'
    )
    backward = InlineKeyboardButton(
        text='<<',
        callback_data='backward'
    )
    buttons = [backward, button_1, button_2, button_3, forward]
    kb_builder.row(*buttons, width=5)

    return kb_builder.as_markup()