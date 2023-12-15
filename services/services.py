import requests

from lexicon.lexicon import lexicon_currency

API_URL = 'https://api.coinlore.net/api/ticker/?id=90,80,48543,2710,54683,58,2,2713,2751,1,33830,118'

def get_course(number: int):
    return requests.get(API_URL).json()[number]['price_usd']

def create_page(number: int):
    result: list = []
    for i in range(0, 3):
        result.append(f'{lexicon_currency[number*3+i]} - {get_course(number*3+1)}')
    return '\n'.join(result)