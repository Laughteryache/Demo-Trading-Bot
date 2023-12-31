from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from config.config import Config, load_config
from data.database import Database
from lexicon.lexicon import ru_lexicon
from keyboards.keyboards import create_inline_kb, PageWithPriceCallbackFactory
from services.services import get_list, FSMContextClass, create_page_of_coin, get_clear_statistics, \
    update_previous_pages

config: Config = load_config()
database = Database(config.database.name)
router = Router()


# MAIN_MENU
@router.callback_query(F.data == 'main_menu')
async def main_menu(callback: CallbackQuery,
                    state: FSMContext):
    keyboard = create_inline_kb(1, 'list', 'briefcase', 'statistics', 'help')

    await state.update_data(previous_pages=['main_menu'])
    await callback.message.edit_text(text=ru_lexicon['main_menu'],
                                     reply_markup=keyboard)


# STOCK MARKET CALLBACK
@router.callback_query(F.data == 'list')
async def stock_market(callback: CallbackQuery,
                       state: FSMContext):
    data = await state.get_data()
    lists: dict = get_list()
    data_callback = callback.data
    data = update_previous_pages(data, data_callback)
    keyboard = create_inline_kb(1, dct=lists, back_button=data['previous_pages'][-1])

    await callback.message.edit_text(text=ru_lexicon['list_of_currency'],
                                     reply_markup=keyboard)
    data['previous_pages'].append(callback.data)
    await state.update_data(previous_pages=data['previous_pages'])


# BRIEFCASE_CALLBACK
@router.callback_query(F.data == 'briefcase')
async def briefcase_page(callback: CallbackQuery,
                         state: FSMContext):
    data = await state.get_data()
    data_callback = callback.data
    data = update_previous_pages(data, data_callback)
    balance, positions = database.get_user_statistics(callback.from_user.id)

    await callback.message.edit_text(text=f"{ru_lexicon['balance'] % round(balance, 2)}\n\n"
                                          f"{ru_lexicon['positions']}\n"
                                          f"{get_clear_statistics(positions)}",
                                     reply_markup=create_inline_kb(1, back_button=data['previous_pages'][-1]))
    data['previous_pages'].append(data_callback)
    await state.update_data(previous_pages=data['previous_pages'])


# STATISTIC_CALLBACK
@router.callback_query(F.data == 'statistics')
async def statistics_page(callback: CallbackQuery,
                          state: FSMContext):
    data = await state.get_data()
    data_callback = callback.data
    data = update_previous_pages(data, data_callback)
    total = database.get_total(callback.from_user.id)

    await callback.message.edit_text(text=ru_lexicon['statistics'] % total,
                                     reply_markup=create_inline_kb(1, back_button=data['previous_pages'][-1]))
    data['previous_pages'].append(data_callback)
    await state.update_data(previous_pages=data['previous_pages'])


# HELP_CALLBACK
@router.callback_query(F.data == 'help')
async def help_callback(callback: CallbackQuery,
                        state: FSMContext):
    data = await state.get_data()
    data_callback = callback.data
    data = update_previous_pages(data, data_callback)

    await callback.message.edit_text(text=ru_lexicon['help'],
                                     reply_markup=create_inline_kb(1, back_button=data['previous_pages'][-1]))


# PAGE_WITH_PRICE_OF_COIN
@router.callback_query(PageWithPriceCallbackFactory.filter())
async def page_with_price_of_one_coin(callback: CallbackQuery,
                                      callback_data: PageWithPriceCallbackFactory,
                                      state: FSMContext):
    data = await state.get_data()
    data_callback = callback.data
    data = update_previous_pages(data, data_callback)
    page = create_page_of_coin(name=callback_data.name_of_coin, price=callback_data.price)
    keyboard = create_inline_kb(1, dct={'buy': 'Купить',
                                        'sell': 'Продать'},
                                back_button=data['previous_pages'][-1])

    await callback.message.edit_text(text=page, reply_markup=keyboard)
    data['previous_pages'].append(callback.data)
    await state.update_data(price=callback_data.price, name_of_coin=callback_data.name_of_coin,
                            previous_pages=data['previous_pages'])
    await state.set_state(default_state)


# BUY_PAGE
@router.callback_query(F.data == 'buy')
async def buy_page(callback: CallbackQuery,
                   state: FSMContext):
    data = await state.get_data()
    price, name_of_coin = data['price'], data['name_of_coin']
    deposit = database.get_user_statistics(callback.from_user.id)[0]
    positions = database.get_user_positions(callback.from_user.id)
    data_callback = callback.data
    data = update_previous_pages(data, data_callback)

    await callback.message.edit_text(text=f"🔻Ваш баланс {round(deposit, 2)}$\n\n"
                                          f"🔻У вас уже куплено {positions[name_of_coin]} {name_of_coin}\n\n"
                                          f"🔻Сколько {name_of_coin} вы хотите купить?",
                                     reply_markup=create_inline_kb(1, back_button=data['previous_pages'][-1]))
    data['previous_pages'].append(callback.data)
    await state.update_data(previous_pages=data['previous_pages'])
    await state.set_state(FSMContextClass.buying)


# SELL_PAGE_CALLBACK
@router.callback_query(F.data == 'sell')
async def sell_page(callback: CallbackQuery,
                    state: FSMContext):
    data = await state.get_data()
    price, name_of_coin = data['price'], data['name_of_coin']
    deposit = database.get_user_statistics(callback.from_user.id)[0]
    positions = database.get_user_positions(callback.from_user.id)
    data_callback = callback.data
    data = update_previous_pages(data, data_callback)

    await callback.message.edit_text(text=f"🔻Ваш баланс {round(deposit, 2)}$\n\n"
                                          f"🔻У вас уже куплено {positions[name_of_coin]} {name_of_coin}\n\n"
                                          f"🔻Сколько {name_of_coin} вы хотите продать?",
                                     reply_markup=create_inline_kb(1, back_button=data['previous_pages'][-1]))
    data['previous_pages'].append(callback.data)
    await state.update_data(price=price, name_of_coin=name_of_coin, previous_pages=data['previous_pages'])
    await state.set_state(FSMContextClass.selling)


# FINAL_BUY_PAGE
@router.callback_query(F.data == 'yes', StateFilter(FSMContextClass.buying))
async def final_buy_page(callback: CallbackQuery,
                         state: FSMContext):
    data = await state.get_data()
    price, name_of_coin, quantity = -1 * float(data['price']), data['name_of_coin'], data['quantity']

    database.update_user_deposit(callback.from_user.id, price, quantity)
    database.update_user_positions(callback.from_user.id, name_of_coin, quantity)
    database.update_total(callback.from_user.id)
    database.update_prices(user_id=callback.from_user.id, price=-1 * price, name_of_coin=name_of_coin)

    deposit = database.get_user_statistics(callback.from_user.id)[0]

    await callback.message.edit_text(text=f"🔻Вы успешно совершили покупку {quantity} {name_of_coin}!\n\n"
                                          f"🔻Ваш баланс {round(deposit, 2)}$",
                                     reply_markup=create_inline_kb(1, 'main_menu'))
    await state.update_data(previous_pages=data['previous_pages'])
    await state.set_state(default_state)


# FINAL_SELL_PAGE
@router.callback_query(F.data == 'yes', StateFilter(FSMContextClass.selling))
async def final_sell_page(callback: CallbackQuery,
                          state: FSMContext):
    data = await state.get_data()
    price, name_of_coin, quantity = float(data['price']), data['name_of_coin'], -1 * int(data['quantity'])

    database.update_user_deposit(callback.from_user.id, price, quantity)
    database.update_user_positions(callback.from_user.id, name_of_coin, quantity)
    database.update_total(callback.from_user.id)

    deposit = database.get_user_statistics(callback.from_user.id)[0]

    await callback.message.edit_text(text=f"🔻Вы успешно совершили продажу {abs(quantity)} {name_of_coin}!\n\n"
                                          f"🔻Ваш баланс {round(deposit, 2)}$",
                                     reply_markup=create_inline_kb(1, 'main_menu'))
    await state.set_state(default_state)


# CLEAR_ALL_PAGE
@router.callback_query(F.data == 'yes', StateFilter(FSMContextClass.clear_all))
async def clear_all_page(callback: CallbackQuery,
                         state: FSMContext):
    database.clear_all(callback.from_user.id)

    await callback.message.edit_text(text=ru_lexicon['successful_clear'],
                                     reply_markup=create_inline_kb(1, 'main_menu'))
    await state.set_state(default_state)
