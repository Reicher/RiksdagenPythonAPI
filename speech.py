import riksdagen


class Speech:
    def __init__(self, data):
        self.data = data
        self.avsnittsrubrik = riksdagen.API.extract(data, 'avsnittsrubrik')
        self.talare = riksdagen.API.extract(data, 'talare')
        self.parti = riksdagen.API.extract(data, 'parti')
        self.replik = riksdagen.API.extract(data, 'replik')

    def print(self):
        print(f'{self.talare} om {self.avsnittsrubrik}. Replik: {self.replik}')
