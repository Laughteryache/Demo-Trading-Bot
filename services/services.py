import requests

API_URL = 'https://api.coinlore.net/api/ticker/?id=90,80,48543'

def get_course(number):
    return requests.get(API_URL).json()[int(number)]['price_usd']