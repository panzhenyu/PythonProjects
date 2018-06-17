# comprehension layer try to convert sentence to three tuples : wordList, intention, attributes

import intentionRecognize
import jieba.posseg as pseg
import re


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
    return 'flight', 1.0


def getSlotValuePair(wordList, intention, SLOTS, RULES):
    retDic = {}
    pos_rules = RULES.get(intention, []).copy()
    pos_slots = SLOTS.get(intention, []).copy()
    for slot in pos_slots:
        retDic[slot] = None
    for slot, regulars in pos_rules.items():
        slot = slot.split(' ')
        group_range = len(slot)

        for reg in regulars:
            match_str = re.match(reg, wordList)                                                 # unable : wordList need to be converted!!
            if match_str == None:
                continue
            for i in range(1, group_range):
                retDic[slot[i]] = match_str.group(i+1)
    return retDic
