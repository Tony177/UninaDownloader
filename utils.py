import crypt
from getpass import getpass
from os import listdir


def filter_cont(content: list, filt: list | tuple) -> list:
    filt_list = []
    for e in content:
        filt_dict = {}
        for key, value in e.items():
            if key in filt:
                filt_dict[key] = value
        filt_list.append(filt_dict)
    return filt_list


def setup() -> dict:
    if "secret.key" not in listdir():
        crypt.gen_key()
    if "credentials.dat" in listdir():
        tmp = crypt.decrypt("credentials.dat")
        return {'username': tmp[0], 'password': tmp[1]}

    else:
        print("Insert Unina Mail: ", end="")
        name = input()
        passwd = getpass("Insert Password: (Password insertion hidden)")
        dat = name + "\n" + passwd
        crypt.encrypt("credentials.dat", dat.encode())
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
