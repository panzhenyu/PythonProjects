# comprehension layer try to convert sentence to three vectors : intention, attributes, text

import IntentionRecognize
import jieba.posseg as pseg


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


def getSlotValuePair(wordList, intention, SLOTS, RULES):
    retDic = {}
    pos_rules = RULES.get(intention, [])
    pos_slots = SLOTS.get(intention, [])
    for slot in pos_slots:
        retDic[slot] = None
    return retDic


def getVector(query, SLOTS, RULES):
    wordList = getWordList(query)
    intention = getIntention(query)
    slot_value_pair = getSlotValuePair(wordList, intention, SLOTS, RULES)
    return (wordList, intention, slot_value_pair)
