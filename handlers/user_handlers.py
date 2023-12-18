from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from data.database import Database
from lexicon.lexicon import handlers_lexicon
from keyboards.keyboards import create_inline_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State

from services.services import FSMContextClass

router = Router()
database = Database('test')

### ###
#######

#START_COMMAND
@router.message(CommandStart(), StateFilter(default_state))
async def start_process(message: Message):
    keyboard = create_inline_kb(1, 'list', 'briefcase', 'statistics', 'help')
    try:
        database.insert_new_user(message.from_user.id)
        await message.answer(text=handlers_lexicon['start'],
                             reply_markup=keyboard)
    except:
        await message.answer(text=handlers_lexicon['start'],
                             reply_markup=keyboard)
#QUANTITY_OF_POSITION
@router.message(StateFilter(FSMContextClass.quantity_of_position))
async def quantity_of_position(message: Message,
                               state: FSMContext):
    if message.text.strip().isdigit():
        text = message.text.strip()
        if database.get_user_deposit(id)>int(message.text.strip())*state.get_data()['price']:
            await message.edit_text(text=f"🔻Вы точно хотите приобрести {text} {state.get_data()['coin']} по цене "
                                         f"{int(text)*state.get_data()['price']}$?",
                                    reply_markup=create_inline_kb(1, 'yes', 'no', 'back'))
        else:
            await message.edit_text(text=f"🔻У вас недостаточно средств",
                                    reply_markup=create_inline_kb(1, 'back_to_menu'))
        await state.set_state(FSMContextClass.process_state)
    else:
        await message.edit_text(text='🔻Вы ввели не число\n\n'
                                     '🔻Пожалуйста, повторите попытку')
#abc
