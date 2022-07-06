from cryptography.fernet import Fernet


def decrypt(filename: str):
    with open("secret.key", "rb") as k:
        key = Fernet(k.read())
    with open(filename, 'rb') as f:
        en_data = f.read()
    return key.decrypt(en_data).decode().split("\n")


def encrypt(filename: str, data: bytes) -> None:
    with open("secret.key", "rb") as k:
        key = Fernet(k.read())
    with open(filename, 'wb') as f:
        f.write(key.encrypt(data))


def gen_key() -> None:
    key = Fernet.generate_key()
    with open("secret.key", 'wb') as kf:
        kf.write(key)
