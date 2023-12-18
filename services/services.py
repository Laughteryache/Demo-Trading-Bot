import requests

from lexicon.lexicon import lexicon_currency

API_URL = 'https://api.coinlore.net/api/ticker/?id=90,80,48543,2710,54683,58,2,2713,2751,1,33830,118'


def get_course():
    return requests.get(API_URL).json()


def get_list() -> dict:
    courses = get_course()
    return {f"🔻Вы уверены, что хотите купить {lexicon_currency[i]} "
                f"по цене {courses[i]['price_usd']}?":
                f'{lexicon_currency[i]} - {courses[i]["price_usd"]}$' for i in range(12)}