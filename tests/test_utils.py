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
def setup_parse():
    material = ["first","second","third","fourth","fifth","sixth","seventh"]
    idx_true = "2-4-6"
    idx_false = "2-4-10"
    idx_single ="5"
    return (material,idx_true,idx_false,idx_single)

@pytest.fixture
def mock_select(setup_select, monkeypatch):
    monkeypatch.setattr('sys.stdin', StringIO('3'))
    selected = utils.select_prof(setup_select)
    return selected


def test_select(mock_select):
    assert mock_select[0] == "carlo" and mock_select[2] == 3

def test_parse(setup_parse,monkeypatch):
    mat,idx_true,idx_false,idx_single = setup_parse
    assert utils.parse_selection(mat,idx_true) == ["second","fourth","sixth"]
    assert utils.parse_selection(mat,idx_single) == ["fifth"]
    assert utils.parse_selection(mat,idx_false) == [-1]

