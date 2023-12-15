import requests

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from data.database import Database
from lexicon.handlers_lexicon import handlers_lexicon

router = Router()
API_URL = "https://api.coinlayer.com/live?621e02b1f8851c52c65f1a062a662e10"
database = Database('test')

#START_COMMAND
@router.message(CommandStart())
async def start_process(message: Message):
    database.insert_new_user(message.from_user.id)
    await message.answer(text=handlers_lexicon['start'])

#HELP_COMMAND
@router.message(Command(commands='help'))
async def help_process(message: Message):
    await message.answer(text=handlers_lexicon['help'])

#STATISTICS_COMMAND
@router.message(Command(commands='statistics'))
async def deposit_process(message: Message):
    user_deposit = database.get_user_deposit(id=message.from_user.id)
    await message.answer(text=f'• Ваш текущий депозит {user_deposit}$')

#LIST_COMMAND
@router.message(Command(commands='list'))
async def send_list(message: Message):
