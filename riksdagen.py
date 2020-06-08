import requests
import logging
from xml.etree.ElementTree import fromstring, ElementTree


class Votering:
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

    def get_voteringar(self, bet='', punkt='', parti='', valkrets='', rost='', antal='500', gruppering=''):

        response = self._get(self.url+'voteringlista/',
                            {'bet': bet, 'punkt': punkt, 'parti': parti, 'valkrests': valkrets, 'iid': '',
                            'rost': rost, 'sz': antal, 'utformat': 'xml', 'gruppering': gruppering})

        tree = ElementTree(fromstring(response.content))
        root = tree.getroot()
        logging.info(f'Got tree root: {root.tag}')

        voteringar = []
        for votering in root:
            data = {}
            for info in votering:
                data[info.tag] = info.text
            voteringar.append(Votering(data))

        return voteringar
        logging.info('Done')






