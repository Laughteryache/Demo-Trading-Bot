import requests

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from data.database import Database
from lexicon.lexicon import handlers_lexicon, ru_lexicon, lexicon_currency
from keyboards.keyboards import menu_keyboard, pagination_keyboard
from services.services import get_course, create_page

router = Router()
API_URL = "https://api.coinlayer.com/live?621e02b1f8851c52c65f1a062a662e10"
database = Database('test2')

#START_COMMAND
@router.message(CommandStart())
async def start_process(message: Message):
    try:
        database.insert_new_user(message.from_user.id)
        await message.answer(text=handlers_lexicon['start'])
    except:
        await message.answer()

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
    await message.answer(text=create_page(0),
                         reply_markup=pagination_keyboard(0))

@router.callback_query(F.data == 'backward')
async def next_page(callback: CallbackQuery):
    page = database.get_user_page(id=callback.from_user.id)
    if page > 0:
        database.update_user_page(id=callback.from_user.id, page=page-1)
        await callback.message.edit_text(text=create_page(page-1),
                                         reply_markup=pagination_keyboard(page-1))
    await callback.answer()

@router.callback_query(F.data == 'forward')
async def next_page(callback: CallbackQuery):
    page = database.get_user_page(id=callback.from_user.id)
    if page < 3:
        database.update_user_page(id=callback.from_user.id, page=page+1)
        await callback.message.edit_text(text=create_page(page+1),
                                         reply_markup=pagination_keyboard(page+1))
    await callback.answer()