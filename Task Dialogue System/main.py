# main process for task dialogue system

import comprehension


def init_sys():
    pass


init_sys()
while (True):
    query = input()
    intention, attribute, textVec = comprehension.getVector(query)
