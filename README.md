# RiksdagenPythonAPI
An python API using the swedish riksdags open data about documents, voting, events and more stuff related to the swedish goverment.

Using data from: 
https://data.riksdagen.se/

## Example Usage

If you don't want to add riksdagen to your syspath you can import the module by: 
```python
import sys
sys.path.append('/home/<username>/Documents/RiksdagenPythonAPI')
import riksdagen
```

Create an instance of the api.
```python
api = riksdagen.API()
```

And get person-data by calling the get_ledamoten.
```python
personer = api.get_ledamoten()
```

You can filter both persons and votes by specifying many parameters. 
```python
voteringar = api.get_voteringar(antal=500, rm='2019/20', parti=p.name, gruppering='namn')
```

