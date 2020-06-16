import riksdagen

api = riksdagen.API()
personer = api.get_ledamoten()
Male = {}
Female = {}
for p in riksdagen.Parti:
    Male[p.name] = 0
    Female[p.name] = 0

for P in personer:
    if not P.kon or not P.parti:
        continue
    if P.kon == 'man':
        Male[P.parti] += 1
    elif P.kon == 'kvinna':
        Female[P.parti] += 1

for p in riksdagen.Parti:
    F = Female[p.name]
    M = Male[p.name]
    try:
        Q = F / (F + M) * 100
    except ZeroDivisionError:
        Q = 100
    print(f'{p.name} har {F} kvinnor och {M} män i riksdagen. {Q:.2f} % kvinnor.')