import requests

API_URL = 'https://api.coinlayer.com/live?access_key=9ea0ffb2097dd48bb95e3515ad27036b'

def get_course(name):
    return requests.get(API_URL).json()['rates'][name]