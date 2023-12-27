import sqlite3

from aiogram import Router
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.types import Message
from data.database import Database
from lexicon.lexicon import handlers_lexicon, ru_lexicon, keyboard_lexicon
from keyboards.keyboards import create_inline_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from services.services import FSMContextClass

router = Router()
database = Database('test')


# START_COMMAND
@router.message(CommandStart(), StateFilter(default_state))
async def start_process(message: Message):
    keyboard = create_inline_kb(1, 'main_menu')
    try:
        database.insert_new_user(message.from_user.id)
        await message.answer(text=handlers_lexicon['start'],
                             reply_markup=keyboard)
    except sqlite3.IntegrityError:
        await message.answer(text=handlers_lexicon['start'],
                             reply_markup=keyboard)


# BUY_HANDLER
@router.message(StateFilter(FSMContextClass.buying))
async def buy_handler(message: Message,
                      state: FSMContext):
    text = message.text.strip()
    data = await state.get_data()

    if message.text.strip().isdigit():
        if database.get_user_statistics(message.from_user.id)[0] > int(text) * float(data['price']):
            await message.answer(text=f"🔻Вы точно хотите приобрести {text} {data['name_of_coin']} по цене "
                                      f"<u>{round(int(message.text.strip()) * float(data['price']), 2)}$</u>?",
                                 reply_markup=create_inline_kb(1, 'yes', back_button=data['previous_pages'][-1]))
            await state.update_data(quantity=int(text))
        else:
            await message.answer(text=f"🔻У вас недостаточно средств",
                                 reply_markup=create_inline_kb(1, 'back_to_menu',
                                                               back_button=data['previous_pages'][-1]))
    else:
        await message.answer(text=f'{ru_lexicon["number_error"]}',
                             reply_markup=create_inline_kb(1, back_button=data['previous_pages'][-1]))


# SELL_HANDLER
@router.message(StateFilter(FSMContextClass.selling))
async def sell_handler(message: Message,
                       state: FSMContext):
    data = await state.get_data()
    text = message.text.strip()

    if message.text.strip().isdigit():
        if float(database.get_user_positions(message.from_user.id)[data['name_of_coin']]) < int(text):
            await message.answer(text=f"🔻У вас недостаточно {data['name_of_coin']}, чтобы продать {text} шт.\n\n",
                                 reply_markup=create_inline_kb(1, dct={'buy': 'Купить'}, back_button='back'))

        else:
            await message.answer(text=f"🔻Вы точно хотите продать {text} {data['name_of_coin']} по цене "
                                      f"<u>{round(int(text) * float(data['price']), 2)}$</u>?",
                                 reply_markup=create_inline_kb(1, 'yes', back_button=data['previous_pages'][-1]))
            await state.update_data(quantity=int(text))
    else:
        await message.edit_text(text=f'{ru_lexicon["number_error"]}',
                                reply_markup=create_inline_kb(1, back_button=data['previous_pages'][-1]))


# CLEAR_ALL_HANDLER
@router.message(Command(commands='clear_all'))
async def clear_all_answer(message: Message,
                           state: FSMContext):
    await state.set_state(FSMContextClass.clear_all)
    await message.answer(text=handlers_lexicon['clear_all'],
                         reply_markup=create_inline_kb(1, 'yes', 'main_menu'))
