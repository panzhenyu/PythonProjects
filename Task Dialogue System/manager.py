import random

class Session(object):
    def __init__(self, intention, slots, credit):
        super(Session)
        self.intention = intention
        self.slots = {}
        for slot in slots:
            self.slots[slot] = None
        self.credit = credit

    def embedValue(self, slot_value):
        for slot, value in slot_value.items():
            self.slots[slot] = value


class SessionManager(object):
    def __init__(self, RESPONSE_PATTERN):
        super(SessionManager)
        self.__sessions = []
        self.__pos = None
        self.__history = []
        self.__RESPONSE_PATTERN = RESPONSE_PATTERN

    def getPos(self):
        return self.__pos

    def manage(self, session, history):
        self.__pos = session
        self.__history.append((history, session.intention))

    def response(self):
        if self.__pos.intention != "chat":
            print("sys : " + self.byPattern())

    def byPattern(self):
        slot = 'None'
        for s, v in self.__pos.slots.items():
            if v == None:
                slot = s
                break
        patterns = self.__RESPONSE_PATTERN[self.__pos.intention][slot]
        res = patterns[int(random.uniform(0, len(patterns)))]                                       # choose response pattern randomly
        if slot == 'None':
            counter = 1
            for slot, value in self.__pos.slots.items():
                res.replace(' ', value, counter)
                counter += 1
        return res
