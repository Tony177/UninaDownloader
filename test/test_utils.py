import pytest
import utils
from io import StringIO


@pytest.fixture
def setup_select():
    d1, d2, d3 = {}, {}, {}
    d1 = {"id": 1, "nome": "mario", "cognome": "rossi", "dipartimento": "dip1"}
    d2 = {"id": 2, "nome": "luigi", "cognome": "verdi"}
    d3 = {"id": 3, "nome": "carlo", "cognome": "blu"}
    return [d1, d2, d3]


@pytest.fixture
def mock_select(setup_select, monkeypatch):
    monkeypatch.setattr('sys.stdin', StringIO('3'))
    selected = utils.select_prof(setup_select)
    return selected


def test_select(mock_select):
    assert mock_select[0] == "carlo" and mock_select[2] == 3
