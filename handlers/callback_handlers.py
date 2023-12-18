from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from data.database import Database
from lexicon.lexicon import handlers_lexicon, ru_lexicon, lexicon_currency
from keyboards.keyboards import create_inline_kb, stockmarket_callback_keyboard, help_callback_keyboard
from services.services import get_list

router = Router()
database = Database('test')


# STOCK_MARKET_CALLBACK
@router.callback_query(F.data == 'list')
async def stock_market(callback: CallbackQuery):
    await callback.message.edit_text(text=ru_lexicon['list_of_currency'],
                                     reply_markup=stockmarket_callback_keyboard)


# STATISTICS_CALLBACK
@router.callback_query(F.data == 'statistics')
async def statistics_answer(callback: CallbackQuery):
    await callback.message.edit_text()


# HELP_CALLBACK
@router.callback_query(F.data == 'help')
async def help_function(callback: CallbackQuery):
    await callback.message.edit_text(text=ru_lexicon['help'],
                                     reply_markup=help_callback_keyboard)
#PURCHASE_CONFIRMATION_CALLBACK
@router.callback_query(F.data.in_())
async def purchase_confirmation(callback: CallbackQuery):
    await callback.message.edit_text(text=)
    print(callback['result']['data'])

#BACKWARD_CALLBACK
@router.message()