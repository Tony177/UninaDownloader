#!/usr/bin/env python
from urllib.parse import quote
from urllib3 import disable_warnings
from os import chdir, listdir, makedirs
from os.path import dirname, realpath
from requests import Session, session
from json import dumps, loads
from cryptography.fernet import Fernet
from getpass import getpass

PROF_FILT = ("id", "dipartimento", "nome", "cognome")
BASE_URL = "https://www.docenti.unina.it/"
DOC_URL = BASE_URL + "webdocenti-be/"
FILE_URL = DOC_URL + "allegati/materiale-didattico/"
LOG_URL = DOC_URL + "auth/login-post-evo/"


class Node():
    def __init__(self) -> None:
        self.path = "/"
        self.name = ""
        self.id = -1
        self.type = "N"  # N none - F file - D directory

    # TODO Implement parent as another Node
    def __init__(self, path: str, name: str, id_: int, type_: str, codins: str) -> None:
        self.path = path
        self.name = name
        self.id = id_
        self.type = type_
        self.codins = codins

    def __repr__(self) -> str:
        c = self.path.count("/")
        if self.path == "/":
            c -= 1
        return "|"+"-"*4*c + " "+self.name


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


def filter_cont(content: list, filt: list | tuple) -> list:
    filt_list = []
    for e in content:
        filt_dict = {}
        for key, value in e.items():
            if key in filt:
                filt_dict[key] = value
        filt_list.append(filt_dict)
    return filt_list


def set_credentials() -> dict:
    if "credentials.dat" in listdir():
        tmp = decrypt("credentials.dat")
        return {'username': tmp[0], 'password': tmp[1]}

    else:
        print("Insert Unina Mail: ", end="")
        name = input()
        passwd = getpass("Insert Password: (Password insertion hidden)")
        dat = name + "\n" + passwd
        encrypt("credentials.dat", dat.encode())
        return {'username': name, 'password': passwd}


def select_prof(name_list: list) -> tuple:
    for i in range(len(name_list)):
        t_n = name_list[i]["nome"]
        t_c = name_list[i]["cognome"]
        if "dipartimento" in name_list[i]:
            t_d = name_list[i]["dipartimento"]
        else:
            t_d = "Don't belong to any department"
        print("{}. {} {} - {}".format(i+1, t_n, t_c, t_d))
    if len(name_list) == 0:
        print("Empty search result.")
        exit(404)
    print("\nSelect ONE professor referring to the index: ", end="")
    idx = int(input())-1
    return (name_list[idx]["nome"], name_list[idx]["cognome"], name_list[idx]["id"])


def explore_mat(s: Session, material: list, directory_tree: list, base_url: str) -> None:
    # {'nome': 'CORSO_DI_RICERCA_OPERATIVA_PER_INGEGNERIA_GESTIONALE', 'id': 34048827, 'pubblica': True, 'libera': True, 'tipo': 'D', 'percorso': '/', 'dataInserimento': 1551716265000, 'cancella': True}
    # <class 'dict'>
    # 5
    if "error" in material:
        return
    for e in material:
        if "codIns" in e:
            codIns = e["codIns"]
        else:
            codIns = ""
        tmp_url = base_url + \
            "{}?codIns={}".format(e["id"], codIns)
        directory_tree.append(
            Node(e["percorso"], e["nome"], int(e["id"]), e["tipo"], codIns))
        if e["percorso"] == "/":
            pth = e["nome"]
        else:
            pth = e["percorso"] + "/"+e["nome"]
            pth = pth[1:]
        if e['tipo'] == 'D':
            print("Access folder: {}".format(e["nome"]))

            makedirs(pth, 0o755, True)
            cont = loads(s.get(tmp_url).text)
            if "contenutoCartella" in cont:
                explore_mat(s, cont["contenutoCartella"],
                            directory_tree, base_url)
        else:
            print("Access file: {}".format(e["nome"]))
            with s.get(FILE_URL+str(e["id"]), stream=True) as req:
                with open(pth, 'wb') as f:
                    for chunk in req.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)


def main():

    cookies = {}
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'Accept': 'application/json, text/plain, */*',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
               "Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/json;charset=utf-8"}
    cred = set_credentials()
    with session() as s:
        r = s.post(url=LOG_URL, json=cred, headers=headers,
                   cookies=cookies, verify=False)
        if r.status_code != 200:
            print("Wrong username/password or server error")
            exit(code=200)

        print("Insert Professor name and surname: ", end="")
        prof_name = quote(input())
        u_search = DOC_URL + f"docenti?nome={prof_name}&0&s=10"
        name_list = filter_cont(loads(s.get(u_search).text)[
                                "content"], PROF_FILT)
        prof = select_prof(name_list)
        id_prof = prof[2]
        prof_dir = "Download/"+prof[0].capitalize() + "_" + prof[1].capitalize()
        makedirs(prof_dir, 0o755, True)
        chdir(prof_dir)
        material_url = DOC_URL + \
            f"docenti/{id_prof}/materiale-didattico/areapubb/?codIns="
        explore_url = DOC_URL + \
            f"docenti/{id_prof}/materiale-didattico/areapubb/"
        material = loads(s.get(material_url).text)
        dic_tree = []
        explore_mat(s, material, dic_tree, explore_url)
        print("\n\t--- Folder Tree ---\n")
        for i in dic_tree:
            print(i)


if __name__ == '__main__':
    disable_warnings()
    chdir(dirname(realpath(__file__)))
    if "secret.key" not in listdir():
        gen_key()
    main()
