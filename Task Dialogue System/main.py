# main process for task dialogue system

import Comprehension

def init_sys():
    print("Welcome to Task Dialogue System!")
    pass


init_sys()
while (True):
    query = input()
    intention, slot_value_pair, textVec = Comprehension.getVector(query)
