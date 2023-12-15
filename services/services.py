import requests

from lexicon.lexicon import lexicon_currency

API_TEMPLATE = 'https://api.coinlore.net/api/ticker/?id='


data_of_courses: dict = {0: '90,80,48543',
                         1: '2710,54683,58',
                         2: '2,2713,2751',
                         3: '1,33830,118'}
def get_course(number: int):
    return requests.get(API_TEMPLATE+data_of_courses[number]).json()


def create_page(number: int) -> str:
    result: list = []
    for i in range(0, 3):
        result.append(f'• <b>{lexicon_currency[number*3+i]}</b> - {get_course(number)[i]["price_usd"]}$')
    return '\n'.join(result)