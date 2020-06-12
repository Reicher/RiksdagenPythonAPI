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
        self.tilltalsnamn = API.extract(data, 'tilltalsnamn')
        self.efternamn = API.extract(data, 'efternamn')
        self.parti = API.extract(data, 'parti')
        self.kon = API.extract(data, 'kon')
        self.fodd_ar = API.extract(data, 'fodd_ar')

    def print(self):
        print(f'{self.tilltalsnamn} {self.efternamn} ({self.parti})')

class API:
    def __init__(self):
        self.url = 'http://data.riksdagen.se/'
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S')

    @staticmethod
    def extract(data, param):
        if not data[param]:
            return None

        value = data[param]
        if value != '-' and value is not None:
            return value
        else:
            return None

    @staticmethod
    def _get(url, sub_url, params):
        response = requests.get(url+sub_url+'/', params=params)

        logging.info(f'Doing request: {response.url + sub_url}')
        if response.status_code != 200:
            logging.error(f'Could not get data from {url}, respons: {response.status_code}')

        data = response.json()[sub_url]
        if data['@hits'] == '0':
            logging.error(f'0 Hits')
            return
        logging.info(f'Successfully got data')
        return data

    def get_ledamoten(self, tilltalsnamn='', efternamn='', kon=''):
        data = self._get(self.url, 'personlista',
                             {'fnamn': tilltalsnamn, 'enamn': efternamn, 'kn': kon,
                              'utformat' : 'json', 'sort': 'sorteringsnamn', 'sortorder': 'asc'})
        if not data:
            return
        person_list = []
        for person_data in data['person']:
            person_list.append(Person(person_data))

        return person_list

    def get_voteringar(self, rm='', bet='', punkt='', parti='', valkrets='', rost='', antal='500', gruppering=''):

        response = self._get(self.url, 'voteringlista',
                            {'rm': rm, 'bet': bet, 'punkt': punkt, 'parti': parti, 'valkrests': valkrets, 'iid': '',
                             'rost': rost, 'sz': antal, 'utformat': 'json', 'gruppering': gruppering, })

        data = response.json()['voteringlista']
        vote_list = []
        for vote_data in data['votering']:
            vote_list.append(Votering(vote_data))

        return vote_list






