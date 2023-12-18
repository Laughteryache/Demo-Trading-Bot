from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from data.database import Database
from lexicon.lexicon import handlers_lexicon
from keyboards.keyboards import create_inline_kb

router = Router()
database = Database('test')

#START_COMMAND
@router.message(CommandStart())
async def start_process(message: Message):
    keyboard = create_inline_kb(1, 'list', 'briefcase', 'statistics', 'help')
    try:
        database.insert_new_user(message.from_user.id)
        await message.answer(text=handlers_lexicon['start'],
                             reply_markup=keyboard)
    except:
        await message.answer(text=handlers_lexicon['start'],
                             reply_markup=keyboard)