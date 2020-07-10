import requests, logging

from vote import Vote
from speech import Speech
from elected import Elected

from enum import Enum
from typing import Dict

logging.basicConfig(level=logging.ERROR)


class Party(Enum):
    V = 0
    S = 1
    MP = 2
    L = 3
    C = 4
    M = 5
    SD = 6
    KD = 7
    NYD = 8


party_name: Dict[Party, str] = {
    Party.V: "Vänsterpartiet",
    Party.S: "Sveriges socialdemokratiska arbetareparti",
    Party.MP: "Miljöpartiet de gröna",
    Party.L: "Liberalerna",
    Party.C: "Centerpartiet",
    Party.M: "Moderata samlingspartiet",
    Party.SD: "Sverigedemokraterna",
    Party.KD: "Kristdemokraterna",
    Party.NYD: "Ny demokrati"
}

riksmoten = ['1993/94', '1994/95', '1995/96', '1996/97', '1997/98', '1998/99', '1999/2000', '2000/01',
             '2001/02', '2002/03', '2003/04', '2004/05', '2005/06', '2006/07', '2007/08', '2008/09', '2009/10',
             '2010/11', '2011/12', '2012/13', '2013/14', '2014/15', '2015/16', '2016/17', '2017/18', '2018/19',
             '2019/20']


class API:
    def __init__(self):
        self.url = 'http://data.riksdagen.se/'

    @staticmethod
    def extract(data, param):
        try:
            if not data or not data[param]:
                return None
        except KeyError:
            logging.warning(f'Got nasty key error when asking for key {param} in our data.')
            return None

        value = data[param]
        if value != '-' and value is not None:
            return value
        else:
            return None

    @staticmethod
    def _get(url, sub_url, params):
        response = requests.get(url+sub_url+'/', params=params)

        logging.info(f'Doing request: {response.url}')
        if response.status_code != 200:
            logging.error(f'Could not get data from {url}, respons: {response.status_code}')

        data = response.json()[sub_url]
        if len(data) == 0:
            logging.error(f'0 Hits')
            return
        logging.info(f'Successfully got data')
        return data

    def get_elected(self, tilltalsnamn='', efternamn='', kon=''):
        data = self._get(self.url, 'personlista',
                         {'fnamn': tilltalsnamn, 'enamn': efternamn, 'kn': kon,
                          'utformat': 'json', 'sort': 'sorteringsnamn', 'sortorder': 'asc'})
        if not data:
            return
        person_list = []
        if data['@hits'] == '0':
            logging.warning(f'No data for.')
        elif data['@hits'] == '1':
            person_list.append(Elected(data['person']))
        else:
            for person_data in data['person']:
                person_list.append(Elected(person_data))

        return person_list

    def get_vote(self, rm='', hangar_id='', bet='', punkt='', parti='', valkrets='', rost='', antal=500, gruppering=''):

        data = self._get(self.url, 'voteringlista',
                         {'hangar_id': hangar_id, 'rm': rm, 'bet': bet, 'punkt': punkt, 'parti': parti,
                          'valkrests': valkrets, 'iid': '', 'rost': rost, 'sz': antal, 'utformat': 'json',
                          'gruppering': gruppering, })

        vote_list = []
        if data['@antal'] == '0':
            logging.warning(f'No data for.')
        elif data['@antal'] == '1':
            vote_list.append(Vote(data['votering']))
        else:
            for vote_data in data['votering']:
                vote_list.append(Vote(vote_data))

        return vote_list

    def get_speech(self, rm='', parti='', anftyp='', antal=100):
        anforande_list = []
        data = self._get(self.url, 'anforandelista',
                         {'rm': rm, 'parti': parti, 'anftyp': anftyp, 'utformat': 'json', 'sz': antal})

        # Only special rule for a party, hate it. Because Folkpartiet changed name to Libreralerna
        if parti == Party.L.name:
            anforande_list += self.get_speech(rm=rm, parti='FP', anftyp=anftyp, antal=antal)

        if not data:
            return anforande_list

        if data['@antal'] == '0':
            logging.warning(f'No data for {rm}, {parti}, {anftyp}')
        elif data['@antal'] == '1':
            anforande_list.append(Speech(data['anforande']))
        else:
            for anforande_data in data['anforande']:
                anforande_list.append(Speech(anforande_data))

        return anforande_list
