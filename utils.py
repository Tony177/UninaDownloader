import crypt
from getpass import getpass
from os import listdir, makedirs
from requests import Session
from json import loads
from signal import signal, SIGINT
from main import FILE_URL

CHUNK_SIZE = 2048


class Node():
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

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_cod(self):
        return self.codins


def signal_handler(sign, frame):
    answ = input("You entered CTRL+C, do you really wanna exit? y/n")
    if answ in ('Y', 'y', 'yes'):
        print("Goodbye!")
        exit(0)


def setup() -> dict[str]:
    """
    Generate secret key and if there isn't any saved credentials, ask them to the user.

        Parameters:
            None

        Returns:
            cred (dict) : {username,password} formatted dictionary
    """
    signal(SIGINT, signal_handler)
    crypt.gen_key()
    if "credentials.dat" in listdir():
        tmp = crypt.decrypt("credentials.dat")
        cred = {'username': tmp[0], 'password': tmp[1]}

    else:
        print("Insert Unina Mail: (with or without @ postfix) ", end="")
        name = input()
        if name.count("@") == 0:
            name += "@studenti.unina.it"
        passwd = getpass("Insert Password (Password insertion hidden):")
        dat = name + "\n" + passwd
        crypt.encrypt("credentials.dat", dat.encode())
        cred = {'username': name, 'password': passwd}
    return cred


def select_prof(name_list: list[dict]) -> tuple[str]:
    """
    Format and print the prof search result and return the choosen one's info

        Parameters:
            name_list (list): List of every professor as dict

        Returns:
            choosen (tuple): 3-value tuple professor composed like (name,surname,index)
    """
    list_lenght = len(name_list)
    for i, e in enumerate(name_list):
        if "dipartimento" in e:
            t_d = e["dipartimento"]
        else:
            t_d = "Don't belong to any department"
        print("{}. {} {} - {}".format(i+1,
              e["nome"].capitalize(), e["cognome"].capitalize(), t_d))
    if list_lenght == 0:
        print("Empty search result.")
        exit(404)
    idx = -1
    while idx > list_lenght-1 or idx < 0:
        print("\nSelect ONE professor referring to the index: ", end="")
        idx = int(input())-1
        if idx > list_lenght-1 or idx < 0:
            print("Please insert a valid index!")
    return (name_list[idx]["nome"], name_list[idx]["cognome"], name_list[idx]["id"])


def parse_selection(material: list, idxs_list: str) -> list:
    sub_material = []
    mat_len = len(material)
    idxs = [int(x) for x in idxs_list.rstrip().split("-")]
    for idx in idxs:
        if idx < 1 or idx > mat_len:
            raise(IndexError)
        sub_material.append(material[idx-1])
    return sub_material


def selection(session: Session, dict_tree: list, base_url: str) -> None:
    """
    Let choose some initial folder or all folder to download, then start calling explore_mat(...)

        Parameters:
            session (Requests.Session): Requests previous authenticated session (with auth cookies)
            base_url (str): standard prefix of the url alredy formatted with the professor id    

        Returns:
            None 
    """
    cont = loads(session.get(base_url).text)  # get the folder content

    for i, e in enumerate(cont):
        print(f'{i+1}. {e["nome"]}')
    print("\nChoose folders inserting index number:")
    choose = input(
        "Multiple with - between, or 'all' to download all: (Ex: 1 / 3-4-5 / all): ")
    if choose in ("All", "ALL", "all"):
        explore_mat(session, cont, dict_tree, base_url)
    else:
        try:
            sub_material = parse_selection(cont, choose)
        except IndexError:
            print("Out of bound selection")
            exit(404)
        explore_mat(session, sub_material, dict_tree, base_url)


def explore_mat(session: Session, material: list, directory_tree: list, base_url: str) -> None:
    """
    Recursively explore remote directory tree, get and download every folder and save its structure in list of nodes

        Parameters:
            session (Requests.Session): Requests previous authenticated session (with auth cookies)
            material (list): list of actual explorable directories/files (text from session's get serialized with json.loads)
            directory_tree (list): IN/OUT list of nodes (to view folders structure)
            base_url (str): standard prefix of the url alredy formatted with the professor id

        Returns:
            None

    """
    for e in material:
        if "codInse" in e:  # Handle case without codIns
            codIns = e["codInse"]
        else:
            codIns = ""
        tmp_url = base_url + \
            "{}?codIns={}".format(
                e["id"], codIns)  # Temp url to explore every child nodes
        directory_tree.append(
            Node(e["percorso"], e["nome"], int(e["id"]), e["tipo"], codIns))  # Saving current node in directory tree
        # Fixing double // on first directory beacuse path was /
        # and file starts with /
        if e["percorso"] == "/":
            pth = e["nome"]
        else:
            pth = e["percorso"] + "/"+e["nome"]
            pth = pth[1:]
        # Replacing _ with space and capitalizing directory name
        pth = pth.replace("_", " ").capitalize()
        if e['tipo'] == 'D':  # if it's a directory
            makedirs(pth, 0o755, True)  # make the folders
            cont = loads(session.get(tmp_url).text)  # get the folder content
            if "contenutoCartella" in cont:  # don't explore if empty or it's an error
                explore_mat(session, cont["contenutoCartella"],
                            directory_tree, base_url)
        else:  # else if it's a file
            print("Downloading file: {}".format(e["nome"]))
            # stream true don't overstress RAM
            with session.get(FILE_URL+str(e["id"]), stream=True) as req:
                with open(pth, 'wb') as f:
                    total_size = int(req.headers.get('Content-Length'))

                    for i, chunk in enumerate(req.iter_content(chunk_size=CHUNK_SIZE)):
                        # progress in % with carriage char to clean previous printed %
                        print("Progress: {:3.2f}%".format(
                            i*CHUNK_SIZE*100/total_size), end='\r')
                        if chunk:
                            f.write(chunk)
