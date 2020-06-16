from typing import Dict

import riksdagen


def get_party_words(api, parti: riksdagen.Parti):

    common_words = {}
    anforande_lista = api.get_anforande(rm='2019/20', parti=parti.name, anftyp='Nej')

    word_list = []
    for anförande in anforande_lista:
        word_list += anförande.avsnittsrubrik.split(" ")

    for word in word_list:
        if word in common_words:
            common_words[word] += 1
        else:
            common_words[word] = 1
    return common_words


api = riksdagen.API()
common_words = get_party_words(api, riksdagen.Parti.V)
print(common_words)
