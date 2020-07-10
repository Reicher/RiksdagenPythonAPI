
import riksdagen


def test_age(self):
    min_age = {}
    max_age = {}
    party_members = {}

    for p in riksdagen.Party:
        min_age[p.name] = 100
        max_age[p.name] = 0
        party_members[p.name] = 0

    api = riksdagen.API()
    personer = api.get_ledamoten()
    for P in personer:
        if not P.parti or not P.fodd_ar:
            continue
        age = (2020 - int(P.fodd_ar))
        if age < min_age[P.parti]:
            min_age[P.parti] = age
        if age > max_age[P.parti]:
            max_age[P.parti] = age
        party_members[P.parti] += 1

    for p in riksdagen.Party:
        print(
            f'{p.name} har {party_members[p.name]} riksdagsledamöten med yngsta {min_age[p.name]} och äldsta {max_age[p.name]}')

    assert False


def test_gender_quota(self):
    api = riksdagen.API()
    personer = api.get_ledamoten()
    Male = {}
    Female = {}
    for p in riksdagen.Party:
        Male[p.name] = 0
        Female[p.name] = 0

    for P in personer:
        if not P.kon or not P.parti:
            continue
        if P.kon == 'man':
            Male[P.parti] += 1
        elif P.kon == 'kvinna':
            Female[P.parti] += 1

    for p in riksdagen.Party:
        F = Female[p.name]
        M = Male[p.name]
        try:
            Q = F / (F + M) * 100
        except ZeroDivisionError:
            Q = 100
        print(f'{p.name} har {F} kvinnor och {M} män i riksdagen. {Q:.2f} % kvinnor.')

    assert False


def test_most_common_words(self):

    api = riksdagen.API()
    common_words = {}
    anforande_lista = api.get_anforande(rm='2019/20', parti=riksdagen.Party.V.name, anftyp='Nej')

    word_list = []
    for anförande in anforande_lista:
        word_list += anförande.avsnittsrubrik.split(" ")

    for word in word_list:
        if word in common_words:
            common_words[word] += 1
        else:
            common_words[word] = 1

    print(common_words)
    assert False


if __name__ == '__main__':
    pass