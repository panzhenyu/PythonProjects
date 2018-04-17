# convert string to text vector
# panda

def textParse(bigString):
    import re
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]


# the document in dataSet must be word list
# convert dataSet to a list without common word
# if you wanna wipe off some words, modify the vocabulary list may be a good choice
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)


# convert sentence to wordVector based on vocabList
def sentence2Vec(vocabList, sentence):
    sentenceVec = [0] * len(vocabList)
    for word in sentence:
        if word in vocabList:
            sentenceVec[vocabList.index(word)] = 1
        else:
            print("the word: %s is not in my Vocabulary" % word)
    return sentenceVec

# convert sentence to wordVector mat
def sentence2Mat(vocabList, sentence):
    wordVecMat = []
    for word in sentence:
        wordVec = [0] * len(vocabList)
        if word in vocabList:
            wordVec[vocabList.index(word)] = 1
        else:
            print("the word: %s is not in my Vocabulary" % word)
        wordVecMat.append(wordVec)
    return wordVecMat
