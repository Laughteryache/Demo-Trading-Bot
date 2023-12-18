import requests
from keyboards.keyboards import PageWithPriceCallbackFactory
from lexicon.lexicon import lexicon_currency
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup

API_URL = 'https://api.coinlore.net/api/ticker/?id=90,80,48543,2710,54683,58,2,2713,2751,1,33830,118'


def get_course():
    return requests.get(API_URL).json()


def get_list() -> dict:
    courses = get_course()
    return {PageWithPriceCallbackFactory(last_page='list', name=lexicon_currency[i], price=f'{courses[i]["price_usd"]}').pack(): f'{lexicon_currency[i]} - {courses[i]["price_usd"]}$' for i in range(12)}

class FSMContextClass(StatesGroup):
    coin = State()
    price = State()
    process_state = State()
    quantity_of_position = State()