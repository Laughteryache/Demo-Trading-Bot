from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from data.database import Database
from lexicon.lexicon import handlers_lexicon
from keyboards.keyboards import menu_keyboard, pagination_keyboard
from services.services import create_page

router = Router()
database = Database('test')


#START_COMMAND
@router.message(CommandStart())
async def start_process(message: Message):
    try:
        database.insert_new_user(message.from_user.id)
        await message.answer(text=handlers_lexicon['start'],
                             reply_keyboard=menu_keyboard)
    except:
        await message.answer(text=handlers_lexicon['start'],
                             reply_keyboard=menu_keyboard)

