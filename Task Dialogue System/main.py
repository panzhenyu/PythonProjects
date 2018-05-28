# main process for task dialogue system

import Comprehension

def init_sys():
    print("Welcome to Task Dialogue System!")
    pass


init_sys()
while (True):
    query = input()
    if query == 'exit':
        break
    vector = Comprehension.getVector(query)
    intention, slot_value_pair, textVec = vector
    print(vector)
