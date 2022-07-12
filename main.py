#!/usr/bin/env python
from urllib.parse import quote
from urllib3 import disable_warnings
from os import chdir, makedirs, remove
from os.path import dirname, realpath
from requests import session, RequestException
from json import loads
import utils

PROF_FILT = ("id", "dipartimento", "nome", "cognome")
BASE_URL = "https://www.docenti.unina.it/"
DOC_URL = BASE_URL + "webdocenti-be/"
FILE_URL = DOC_URL + "allegati/materiale-didattico/"
LOG_URL = DOC_URL + "auth/login-post-evo/"
DOWNLOAD_PATH = "download/"


def main():
    cookies = {}
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'Accept': 'application/json, text/plain, */*',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36\
                (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
               "Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip,\
                deflate"}
    # Generate secret if not present and retrive from file or stdin credentials
    cred = utils.setup()
    try:
        with session() as s:
            # Login and get token cookie
            r = s.post(url=LOG_URL, json=cred, headers=headers,
                       cookies=cookies, verify=False)
            if r.status_code != 200:
                remove("credentials.dat")
                print("Wrong username/password or server error")
                exit(code=200)
            while True:
                print("Insert Professor name and surname: (0 to exit)", end="")

                prof_name = quote(input())
                if prof_name == '0':
                    print("Goodbye!")
                    exit(0)
                u_search = DOC_URL + f"docenti?nome={prof_name}&0&s=10"
                name_list = loads(s.get(u_search).text)["content"]
                prof = utils.select_prof(name_list)
                id_prof = prof[2]
                prof_dir = DOWNLOAD_PATH + \
                    prof[0].capitalize() + " " + prof[1].capitalize()
                makedirs(prof_dir, 0o755, True)
                chdir(prof_dir)
                explore_url = DOC_URL + \
                    f"docenti/{id_prof}/materiale-didattico/areapubb/"
                material_url = explore_url + "?codIns="

                material = loads(s.get(material_url).text)
                dic_tree = []
                utils.selection(s, dic_tree, explore_url)
                # utils.explore_mat(s, material, dic_tree, explore_url)
                print("\n\t--- Folder Tree ---\n")
                for d in dic_tree:
                    print(d)
    except RequestException as e:
        print("Connection error, check your internet.")
        with open("error.txt", 'w') as f:
            f.write(str(e))
        exit(-1)


if __name__ == '__main__':
    disable_warnings()  # Disable SSL certificate warning
    chdir(dirname(realpath(__file__))) # Set project root folder as working directory
    main()
