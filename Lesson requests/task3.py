import os
import requests
from pprint import pprint
import datetime

class SOF:
    def __init__(self):
        pass

    def get_last_questions(self, tag='Python', day_period=2):
        # Получение ссылки для загрузки файла
        url = 'https://api.stackexchange.com/2.3/questions'
        params = {
            'tagged': tag,
            'site': 'stackoverflow',
            'datefrom': datetime.datetime.today() - datetime.timedelta(days=day_period)
        }
        result = requests.get(url, params=params).json()
        pprint(result)

if __name__ == '__main__':
    stackoverflow_request = SOF()
    result = stackoverflow_request.get_last_questions()
