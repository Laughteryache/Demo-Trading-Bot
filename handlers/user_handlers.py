import requests

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from data.database import Database
from lexicon.lexicon import handlers_lexicon, ru_lexicon, lexicon_currency
from keyboards.keyboards import menu_keyboard, courses_keyboard
from services.services import get_course

router = Router()
API_URL = "https://api.coinlayer.com/live?621e02b1f8851c52c65f1a062a662e10"
database = Database('test')

#START_COMMAND
@router.message(CommandStart())
async def start_process(message: Message):
    database.insert_new_user(message.from_user.id)
    await message.answer(text=handlers_lexicon['start'], reply_markup=menu_keyboard)

#HELP_COMMAND
@router.message(Command(commands='help'))
async def help_process(message: Message):
    await message.answer(text=handlers_lexicon['help'])

#STATISTICS_COMMAND
@router.message(Command(commands='statistics'))
async def deposit_process(message: Message):
    user_deposit = database.get_user_statistics(id=message.from_user.id)
    await message.answer(text=f'• Ваш текущий депозит {user_deposit}$')

#LIST_COMMAND
@router.message(Command(commands='list'))
async def send_list(message: Message):
    await message.answer(text=ru_lexicon['list_of_currency'],
                         reply_markup=courses_keyboard)

#CALLBACKS_LIST_OF_CURRENCY
@router.callback_query(F.data.in_(['0',
                                  '1',
                                  '2']))
async def selected_currency(callback: CallbackQuery):
    course = get_course(callback.data)
    await callback.message.edit_text(text=f'• Курс {lexicon_currency[callback.data]} к доллару:\n'
                                          f'{course} $')

# ILYA