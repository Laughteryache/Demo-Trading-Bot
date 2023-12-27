import requests
from aiogram import Bot
from aiogram.types import BotCommand

from keyboards.keyboards import PageWithPriceCallbackFactory
from lexicon.lexicon import lexicon_currency, lexicon_for_page_of_coin, menu_commands
from aiogram.fsm.state import State, StatesGroup


API_URL = 'https://api.coinlore.net/api/ticker/?id=90,80,48543,2710,54683,58,2,2713,2751,1,33830,118'


def get_course():
    return requests.get(API_URL).json()


def get_list() -> dict:
    courses = get_course()
    return {PageWithPriceCallbackFactory(name_of_coin=lexicon_currency[i], price=f'{courses[i]["price_usd"]}').pack(): f'{lexicon_currency[i]} - {courses[i]["price_usd"]}$' for i in range(12)}


def get_courses() -> dict:
    courses = get_course()
    return {lexicon_currency[i]: courses[i]["price_usd"] for i in range(12)}


def create_page_of_coin(name, price) -> str:
    return lexicon_for_page_of_coin % (name, price)


def get_clear_statistics(data: list) -> str:
    result = []
    for i in data:
        if '0' != i.split('-')[1]:
            result.append(f"""•{i} шт.""")
    if result:
        return '\n'.join(result)
    else:
        return "На данный момент у вас нету\nоткрытых позиций"


class FSMContextClass(StatesGroup):
    previous_pages = State()
    price = State()
    name_of_coin = State()
    buying = State()
    selling = State()
    quantity = State()
    clear_all = State()


async def set_menu_commands(bot: Bot):
    main_menu = [
        BotCommand(command=command, description=description) for command, description in menu_commands.items()
    ]
    await bot.set_my_commands(main_menu)


def update_previous_pages(data, callback_data):
    if callback_data in data['previous_pages']:
        del data['previous_pages'][-1]
        del data['previous_pages'][-1]
    return data
