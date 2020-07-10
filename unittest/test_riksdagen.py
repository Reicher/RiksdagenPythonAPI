import json
from unittest.mock import Mock

import pytest
import riksdagen


@pytest.fixture
def api_fixture():
    mock_api = Mock(spec=riksdagen.API)
    return mock_api


def get_data():
    with open('data.json') as json_file:
        return json.load(json_file)


def test_extract(api_fixture):
    data = get_data()
    person_data = data['personlista']['person']

    hangar_id = api_fixture.extract(person_data, 'hangar_id')
    assert hangar_id == '2343623'

    weird = api_fixture.extract(person_data, '123456789')
    assert weird is None


def test_get_elected(api_fixture):
    api_fixture._get.return_value = get_data()

    elected = api_fixture.get_elected()  # Should return a lot more usually

    assert api_fixture._get.assert_called_once()
    assert elected is not None
    assert elected[0].tilltalsnamn == 'Ali'



#def test_get_vote(api_fixture):
#    assert False


#def test_get_speech(api_fixture):
#    assert False