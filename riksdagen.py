import requests
import logging
from enum import Enum


class Parti(Enum):
    V = 0
    S = 1
    MP = 2
    L = 3
    C = 4
    M = 5
    SD = 6
    KD = 7


class Votering:
    def __init__(self, data):
        self.data = data

    def print(self):
        text = ''
        for key, value in self.data.items():
            text += f'{key}: {value}\n'
        print(text)


class Person:
    def __init__(self, data):
        self.data = data

    def print(self):
        text = ''
        for key, value in self.data.items():
            text += f'{key}: {value}\n'
        print(text)

class API:
    def __init__(self):
        self.url = 'http://data.riksdagen.se/'
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S')

    @staticmethod
    def _get(url, params):
        response = requests.get(url, params=params)

        logging.info(f'Get request: {response.url}')
        if response.status_code != 200:
            logging.error(f'Could not get data from {url}, respons: {response.status_code}')

        return response

    def get_ledamoten(self):
        response = self._get(self.url + 'personlista/',
                             {'utformat' : 'json', 'sort': 'sorteringsnamn', 'sortorder': 'asc'})

        data = response.json()['personlista']
        person_list = []
        for person_data in data['person']:
            person_list.append(Person(person_data))

        return person_list

    def get_voteringar(self, rm='', bet='', punkt='', parti='', valkrets='', rost='', antal='500', gruppering=''):

        response = self._get(self.url+'voteringlista/',
                            {'rm': rm, 'bet': bet, 'punkt': punkt, 'parti': parti, 'valkrests': valkrets, 'iid': '',
                             'rost': rost, 'sz': antal, 'utformat': 'json', 'gruppering': gruppering, })

        data = response.json()['voteringlista']
        vote_list = []
        for vote_data in data['votering']:
            vote_list.append(Votering(vote_data))

        return vote_list






