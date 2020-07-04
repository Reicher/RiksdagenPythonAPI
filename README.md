# RiksdagenPythonAPI
An python API using the swedish riksdags open data about documents, voting, events and more stuff related to the swedish goverment.

Using data from: 
https://data.riksdagen.se/

## Requirements
Are specified in the requirements.txt. Some extra stuff you dont need *might* be there. 
Get them by running:
```console
$ pip install -r requirements.txt
```

## Example Usage

Create an instance of the api.
```python
import riksdagen

api = riksdagen.API()
```

And get person-data by calling the get_ledamoten.
```python
personer = api.get_ledamoten()
```

You can filter both persons and votes by specifying a couple of parameters. 
```python
voteringar = api.get_voteringar(antal=500, rm='2019/20', parti=p.name, gruppering='namn')
```

To get an anföranden use get_anforande and add a couple of parameters if you want.  
```python
anforande_lista = api.get_anforande(rm='2019/20', parti=parti.name, anftyp='Nej')
```