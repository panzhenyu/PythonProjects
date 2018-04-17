# main process for task dialogue system

import Comprehension


def init_sys():
    pass


init_sys()
while (True):
    query = input()
    intention, attribute, textVec = Comprehension.getVector(query)
