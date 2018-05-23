# comprehension layer try to convert sentence to three vectors : intention, attributes, text

import IntentionRecognize
import jieba.posseg as pseg

def init():
    global RULE
    RULE = {}


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
    return "flight"



def getSlotValuePair(wordList, intention):
    retDic = {}
    if intention == 'fligth':
        pass
    return retDic


def getVector(text):
    init()
    wordList = getWordList(text)
    intention = getIntention(text)
    slot_value_pair = getSlotValuePair(wordList, intention)
    return (wordList, intention, slot_value_pair)

init()
print(RULE)