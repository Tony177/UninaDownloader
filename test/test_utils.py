import pytest
import utils


@pytest.fixture
def setup_select():
    d1, d2, d3 = {}, {}, {}
    d1 = {"nome": "mario", "cognome": "rossi", "dipartimento": "dip1"}
    d2 = {"nome": "luigi", "cognome": "verdi"}
    d3 = {"nome": "carlo", "cognome": "blu"}
    return [d1, d2, d3]

# TODO Fix ovveride input function in order to test select_prof
# @pytest.fixture
# def mock_select(setup_select,monkeypatch):
#     monkeypatch.setattr('builtins.input', lambda _ : '1')
#     selected = utils.select_prof(setup_select)
#     return selected

# def test_select(mock_select):
#     assert mock_select["nome"] == "carlo" and mock_select["dipartimento"] == "" 
