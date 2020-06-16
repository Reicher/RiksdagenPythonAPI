import riksdagen

min_age = {}
max_age = {}
party_members = {}

for p in riksdagen.Parti:
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

for p in riksdagen.Parti:
    print(
        f'{p.name} har {party_members[p.name]} riksdagsledamöten med yngsta {min_age[p.name]} och äldsta {max_age[p.name]}')