from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from data.database import Database
from lexicon.lexicon import handlers_lexicon, ru_lexicon
from keyboards.keyboards import create_inline_kb, PageWithPriceCallbackFactory
from services.services import get_list, FSMContextClass


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

@router.callback_query(PageWithPriceCallbackFactory.filter())
async def buy_page(callback: CallbackQuery,
                   callback_data: PageWithPriceCallbackFactory,
                   state: FSMContext):
    price, name = callback_data.price, callback_data.name
    deposit = database.get_user_deposit(callback.from_user.id)
    positions = database.get_user_positions(callback.from_user.id)
    await callback.message.edit_text(text=f"🔻Ваш баланс {deposit}$\n\n"
                                          f"🔻У вас уже куплено {positions[name]} {name}\n\n"
                                          f"🔻Сколько {name} вы хотите купить?",
                                     reply_markup=create_inline_kb(1, 'back'))
    await state.update_data(coin=name, price=price)
    await state.set_state(FSMContextClass.quantity_of_position)