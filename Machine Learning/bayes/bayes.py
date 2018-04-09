# machine learning algorithm for bayes
# panda
# -*- coding: utf-8 -*-
from numpy import *
import operator


# create a dataSet
def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmatian', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]
    return postingList, classVec


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


# convert sentence to bag of words vector based on vocabList
def bagOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec


# calculate the frequency of words, return the most frequent words
# default size is 30
def calcMostFreq(vocabList, fullText, size=30):
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sortedFreq = sorted(freqDict.items(), key=operator.itemgetter(1), reverse=True)
    return sortedFreq[0:size]


# training, return the word frequency vector of classes and frequency of class 1
# default class is 1 and 0, modify code to support multi-classes
def trainNBO(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Den = 2.0
    p1Den = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Den += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Den += sum(trainMatrix[i])
    p1Vec = log(p1Num / p1Den)
    p0Vec = log(p0Num / p0Den)
    return p0Vec, p1Vec, pAbusive


# use returned args of trainNBO to classify
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0


# test bayes based on loadDataSet()
def testingNB():
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for doc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, doc))
    p0V, p1V, pAb = trainNBO(trainMat, listClasses)
    testEntry = [['love', 'my', 'dalmatian'], ['stupid', 'garbage']]
    for test in testEntry:
        thisDoc = array(setOfWords2Vec(myVocabList, test))
        print(test, 'classified as:', classifyNB(thisDoc, p0V, p1V, pAb))


# test bayes based on email
def spamTest():
    docList = []
    classList = []
    for i in range(1, 26):
        wordList = textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    trainingSet = range(50)
    testSet = []
    for i in range(10):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del (trainingSet[randIndex])
    trainMat = []
    trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V, p1V, pSpam = trainNBO(trainMat, trainClasses)
    errorCounts = 0
    for docIndex in testSet:
        testDoc = bagOfWords2Vec(vocabList, docList[docIndex])
        returnedClass = classifyNB(testDoc, p0V, p1V, pSpam)
        if returnedClass != classList[docIndex]:
            errorCounts += 1
    print('the error rate is:', float(errorCounts) / len(testSet))


# test bayes based on feedparser resource
def localWords(feed0, feed1):
    docList = []
    classList = []
    fullText = []
    len0 = len(feed0['entries'])
    len1 = len(feed1['entries'])
    minLen = min((len0, len1))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    top30Words = calcMostFreq(vocabList, fullText, 30)
    for word in top30Words:
        if word[0] in vocabList:
            vocabList.remove(word[0])
    trainingSet = range(2 * minLen)
    testSet = []
    for i in range(20):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del (trainingSet[randIndex])
    trainMat = []
    trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V, p1V, pSpam = trainNBO(trainMat, trainClasses)
    errorCount = 0
    for docIndex in testSet:
        docVec = bagOfWords2Vec(vocabList, docList[docIndex])
        returnClass = classifyNB(docVec, p0V, p1V, pSpam)
        if returnClass != classList[docIndex]:
            errorCount += 1
    print("the error rate is:", float(errorCount) / len(testSet))

spamTest()