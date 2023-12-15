from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import keyboard_lexicon, lexicon_currency

#MENU_KEYBOARD
menu_keyboard_builder = ReplyKeyboardBuilder()
menu_buttons = [KeyboardButton(text=i) for i in keyboard_lexicon['menu'].items()]
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

def pagination_keyboard(number: int) -> InlineKeyboardMarkup:
    button_1 = InlineKeyboardButton(
        text=f'{lexicon_currency[number*3]}/USDT',
        callback_data=str(number*3)
    )
    button_2 = InlineKeyboardButton(
        text=f'{lexicon_currency[number*3+1]}/USDT',
        callback_data=str(number*3+1)
    )
    button_3 = InlineKeyboardButton(
        text=f'{lexicon_currency[number*3+2]}/USDT',
        callback_data=str(number*3+2)
    )
    if number<3:
        forward = InlineKeyboardButton(
            text='>>',
            callback_data='forward'
        )
    else:
        forward = InlineKeyboardButton(
            text='>>',
            callback_data='empty'
        )
    if number>0:
        backward = InlineKeyboardButton(
            text='<<',
            callback_data='backward'
        )
    else:
        backward = InlineKeyboardButton(
            text='<<',
            callback_data='empty'
        )
    courses_keyboard = InlineKeyboardMarkup(inline_keyboard=[[backward], [button_1], [button_2], [button_3], [forward]])