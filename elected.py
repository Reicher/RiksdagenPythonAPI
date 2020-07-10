import riksdagen


class Elected:
    def __init__(self, data):
        self.data = data
        self.tilltalsnamn = riksdagen.API.extract(data, 'tilltalsnamn')
        self.efternamn = riksdagen.API.extract(data, 'efternamn')
        self.parti = riksdagen.API.extract(data, 'parti')
        self.kon = riksdagen.API.extract(data, 'kon')
        self.fodd_ar = riksdagen.API.extract(data, 'fodd_ar')

    def print(self):
        print(f'{self.tilltalsnamn} {self.efternamn} ({self.parti})')
