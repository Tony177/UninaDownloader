import crypt
import pytest
from os import listdir, remove, chdir
from os.path import dirname, realpath


@pytest.fixture(scope="module")
def setup():
    chdir(dirname(realpath(__file__)))
    crypt.gen_key()
    yield
    remove("secret.key")
    remove("test.dat")


@pytest.fixture
def tmp_file_dec():
    with open("test.txt", 'w+') as f:
        f.write("Test\nDone")
        file = f.read()
    yield file
    remove("test.txt")


def test_gen(setup):
    assert "secret.key" in listdir()


def test_encrypt(setup):
    crypt.encrypt("test.dat", "Test\nDone".encode())
    assert "test.dat" in listdir()


def test_decrypt(tmp_file_dec, setup):
    dec = crypt.decrypt("test.dat")
    assert " ".join(dec) == "Test Done"
