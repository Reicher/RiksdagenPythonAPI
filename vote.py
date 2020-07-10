import riksdagen


class Vote:
    def __init__(self, data):
        self.data = data
        self.namn = riksdagen.API.extract(data, 'namn')
        #self.ja = API.extract(data, 'Ja')
        #self.nej = API.extract(data, 'Nej')
        #self.franfarande = API.extract(data, 'Frånvarande')
        #self.avstar = API.extract(data, 'Avstår')

    def print(self):
        print(f'{self.namn}')