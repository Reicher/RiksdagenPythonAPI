import requests
import logging
from enum import Enum
from typing import Dict


class Parti(Enum):
    V = 0
    S = 1
    MP = 2
    L = 3
    C = 4
    M = 5
    SD = 6
    KD = 7


parti_namn: Dict[Parti, str] = {
    Parti.V: "Vänsterpartiet",
    Parti.S: "Sveriges socialdemokratiska arbetareparti ",
    Parti.MP: "Miljöpartiet de gröna",
    Parti.L: "Liberalerna",
    Parti.C: "Centerpartiet",
    Parti.M: "Moderata samlingspartiet",
    Parti.SD: "Sverigedemokraterna",
    Parti.KD: "Kristdemokraterna"
}


class Votering:
    def __init__(self, data):
        self.data = data
        self.namn = API.extract(data, 'namn')
        self.ja = API.extract(data, 'Ja')
        self.nej = API.extract(data, 'Nej')
        self.franfarande = API.extract(data, 'Frånvarande')
        self.avstar = API.extract(data, 'Avstår')

    def print(self):
        print(f'{self.namn}')


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

class Anforande:
    def __init__(self, data):
        self.data = data
        self.avsnittsrubrik = API.extract(data, 'avsnittsrubrik')
        self.talare = API.extract(data, 'talare')
        self.parti = API.extract(data, 'parti')
        self.replik = API.extract(data, 'replik')

    def print(self):
        print(f'{self.talare} om {self.avsnittsrubrik}. Replik: {self.replik}')


class API:
    def __init__(self):
        self.url = 'http://data.riksdagen.se/'

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
        if len(data) == 0:
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

    def get_voteringar(self, rm='', bet='', punkt='', parti='', valkrets='', rost='', antal=500, gruppering=''):

        data = self._get(self.url, 'voteringlista',
                            {'rm': rm, 'bet': bet, 'punkt': punkt, 'parti': parti, 'valkrests': valkrets, 'iid': '',
                             'rost': rost, 'sz': antal, 'utformat': 'json', 'gruppering': gruppering, })

        vote_list = []
        for vote_data in data['votering']:
            vote_list.append(Votering(vote_data))

        return vote_list

    def get_anforande(self, rm='', parti='', anftyp='', antal=100):
        data = self._get(self.url, 'anforandelista',
                             {'rm': rm, 'parti': parti, 'anftyp': anftyp,
                              'utformat' : 'json', 'sz': antal})
        if not data:
            return
        anforande_list = []
        for anforande_data in data['anforande']:
            anforande_list.append(Anforande(anforande_data))
        return anforande_list




