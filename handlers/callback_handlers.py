from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from data.database import Database
from lexicon.lexicon import handlers_lexicon, ru_lexicon
from keyboards.keyboards import create_inline_kb
from services.services import get_list

router = Router()
database = Database('test')


# STOCK MARKET CALLBACK
@router.callback_query(F.data == 'list')
async def stock_market(callback: CallbackQuery):
    lists: dict = get_list()
    keyboard = create_inline_kb(1, last_btn='back', dct=lists)
    await callback.message.edit_text(text=ru_lexicon['list_of_currency'], reply_markup=keyboard)


# STATISTICS_CALLBACK
@router.callback_query(F.data == 'statistics')
async def statistics_answer(callback: CallbackQuery):
    await callback.message.edit_text()


# HELP_CALLBACK
@router.callback_query(F.data == 'help')
async def help_function(callback: CallbackQuery):
    await callback.message.edit_text(text=ru_lexicon['help'],
                                     reply_markup=create_inline_kb(1, 'back'))
