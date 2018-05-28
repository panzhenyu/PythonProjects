# comprehension layer try to convert sentence to three vectors : intention, attributes, text

import IntentionRecognize
import jieba.posseg as pseg
import xml.dom.minidom

def init():
    global RULES
    global SLOTS
    RULES = {}
    SLOTS = {}
    intentions_dom = xml.dom.minidom.parse(r'./Knowledge/Intentions_slot_pattern.xml')
    intentions_root = intentions_dom.documentElement
    intentions_elem = intentions_root.getElementsByTagName('intention')
    if intentions_elem == None:
        print("no intention knowledge")
        return
    for intention in intentions_elem:
        type = intention.getAttribute('type')
        slots = [intention.childNode[i] for i in range(len(intention.childNode)) if isinstance(intention.childNode[i], xml.dom.minidom.Element)]
        s_name = [slots[i].getAttribute('name') for i in range(len(slots))]
        s_pattern = [slots[i].getElementsByTagName('name') for i in range(len(slots))]

    SLOTS['flight'] = ['ori', 'dst', 'time', 'price']


def preTreat(sentence):
    ignored_chars = r".,?:;''""\\<>!~`$#，。’‘“”？、`"
    preTreated = ""
    for char in sentence:
        if char not in ignored_chars:
            preTreated += char
    return preTreated


def getWordList(text):
    text = preTreat(text)
    words = list(pseg.cut(text))
    return words


def getIntention(text):
    return 'flight'



def getSlotValuePair(wordList, intention):
    retDic = {}
    pos_rules = RULES.get(intention, [])
    pos_slots = SLOTS.get(intention, [])
    for slot in pos_slots:
        retDic[slot] = None
    return retDic


def getVector(text):
    init()
    wordList = getWordList(text)
    intention = getIntention(text)
    slot_value_pair = getSlotValuePair(wordList, intention)
    return (wordList, intention, slot_value_pair)
