# main process for task dialogue system

import comprehension
import xml.dom.minidom
from manager import SessionManager, Session

def load_IntentionInfo():

    global SLOTS
    global RULES
    global RESPONSE_PATTERN
    SLOTS = {}
    RULES = {}
    RESPONSE_PATTERN = {}

    intentions_dom = xml.dom.minidom.parse(r'./resource/IntentionInfo.xml')
    intentions_root = intentions_dom.documentElement
    intentions_elem = intentions_root.getElementsByTagName('intention')
    if intentions_elem == None:
        print("no intention knowledge")
        return

    for intention in intentions_elem:
        type = intention.getAttribute('type')

        slots = intention.getAttribute('slots').split(' ')
        while '' in slots:
            slots.remove('')

        pattern = {}
        match_pattern = intention.getElementsByTagName('match-pattern')
        for p in match_pattern:
            match_slots = p.getAttribute('slots')
            contents = p.childNodes[0].data.split('\n')
            contents = [contents[i].strip(' ') for i in range(len(contents))]
            while '' in contents:
                contents.remove('')
            pattern[match_slots] = contents

        model = {}
        response_model = intention.getElementsByTagName('response-model')
        for m in response_model:
            res_slots = m.getAttribute('slots')
            contents = m.childNodes[0].data.split('\n')
            contents = [contents[i].strip(' ') for i in range(len(contents))]
            while '' in contents:
                contents.remove('')
            model[res_slots] = contents

        SLOTS[type] = slots
        RULES[type] = pattern
        RESPONSE_PATTERN[type] = model

    print(SLOTS)
    print(RULES)
    print(RESPONSE_PATTERN)


def load_Models():
    pass


def init_sys():
    print("Welcome to Task Dialogue System!")
    load_IntentionInfo()
    load_Models()


def close_sys():
    print("bye")


if __name__ == '__main__':

    init_sys()
    manager = SessionManager(RESPONSE_PATTERN)

    while (True):
        query = input()
        if query == 'exit':
            break

        textVec = comprehension.getWordList(query)
        intention, credit = comprehension.getIntention(query)
        sess = Session(intention, SLOTS[intention], credit)                                             # create session

        manager.manage(sess, textVec)                                                                   # manage session
        posIntention = manager.getPos()

        slot_value_pair = comprehension.getSlotValuePair(textVec, posIntention.intention, SLOTS, RULES) # get slot value
        posIntention.embedValue(slot_value_pair)                                                        # embed slot by value

        print((textVec, intention, slot_value_pair))
        manager.response()                                                                              # response to user

    close_sys()
