from cryptography.fernet import Fernet
from os import listdir


def decrypt(filename: str) -> list[str]:
    """
    Decrypt a file with the secret file key

        Parameters:
            filename (str): file's name to decode, including extension

        Returns:
             dec_data (list): 2-value list credentials composed like [username,password]
    """
    with open("secret.key", "rb") as k:
        key = Fernet(k.read())
    with open(filename, 'rb') as f:
        en_data = f.read()
    return key.decrypt(en_data).decode().split("\n")


def encrypt(filename: str, data: bytes) -> None:
    """
    Encrypt a file with the secret file key

        Parameters:
            filename (str): file's name to save, including exstension
            data (bytes): data's byte to encrypt

        Returns:
            None
    """
    with open("secret.key", "rb") as k:
        key = Fernet(k.read())
    with open(filename, 'wb') as f:
        f.write(key.encrypt(data))


def gen_key() -> None:
    """
        Secret key generation if doesn't alredy exist
    """
    if "secret.key" not in listdir():
        key = Fernet.generate_key()
        with open("secret.key", 'wb') as kf:
            kf.write(key)
