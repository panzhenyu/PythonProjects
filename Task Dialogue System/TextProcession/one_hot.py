# convert string to text vector
def textParse(bigString):
    import re
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]


# convert dataSet to a list without common word
# if you wanna wipe off some words, modify the vocabulary list may be a good choice
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)


# convert sentence to wordVector based on vocabList
def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word: %s is not in my Vocabulary" % word)
    return returnVec

def setOfWords2Mat(vocabList, inputSet):
    returnMat = []
    for word in inputSet:
        wordVec = [0] * len(vocabList)
        if word in vocabList:
            wordVec[vocabList.index(word)] = 1
        else:
            print("the word: %s is not in my Vocabulary" % word)
        returnMat.append(wordVec)
    return returnMat