#!/usr/bin/env python
from urllib.parse import quote
from urllib3 import disable_warnings
from os import chdir, makedirs,remove
from os.path import dirname, realpath
from requests import Session, session
from json import loads
import utils

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
            makedirs(pth, 0o755, True)
            cont = loads(s.get(tmp_url).text)
            if "contenutoCartella" in cont:
                explore_mat(s, cont["contenutoCartella"],
                            directory_tree, base_url)
        else:
            print("Downloading file: {}".format(e["nome"]))
            with s.get(FILE_URL+str(e["id"]), stream=True) as req:
                with open(pth, 'wb') as f:
                    total_size = int(req.headers.get('Content-Length'))
                    for i,chunk in enumerate(req.iter_content(chunk_size=1024)):
                        print("Progress: {:3.2f}%".format(i*1024*100/total_size),end='\r')
                        if chunk:
                            f.write(chunk)


def main():
    cookies = {}
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'Accept': 'application/json, text/plain, */*',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
               "Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/json;charset=utf-8"}
    cred = utils.setup()
    with session() as s:
        r = s.post(url=LOG_URL, json=cred, headers=headers,
                   cookies=cookies, verify=False)
        if r.status_code != 200:
            remove("credentials.dat")
            print("Wrong username/password or server error")
            exit(code=200)

        print("Insert Professor name and surname: ", end="")
        prof_name = quote(input())
        u_search = DOC_URL + f"docenti?nome={prof_name}&0&s=10"
        name_list = utils.filter_cont(loads(s.get(u_search).text)[
            "content"], PROF_FILT)
        prof = utils.select_prof(name_list)
        id_prof = prof[2]
        prof_dir = "Download/" + \
            prof[0].capitalize() + "_" + prof[1].capitalize()
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
    main()
