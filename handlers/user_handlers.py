import requests

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from data.database import Database
from lexicon.handlers_lexicon import handlers_lexicon

router = Router()
database = Database()

#START_COMMAND
@router.message(CommandStart())
async def start_process(message: Message):
    database.insert_new_user(message.from_user.id)
    await message.answer(text=handlers_lexicon['start'])


