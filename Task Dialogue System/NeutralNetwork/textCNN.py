# cnn for text classification
# panda
# -*- coding: utf-8 -*-
from TextProcession import one_hot
from numpy import *
from NeutralNetwork import bpnn


class textCNN:
    def __init__(self, vecLen, filter_width, filterStep, nh, nh_layer, no):
        self.vecLen = vecLen
        self.filterWidth = filter_width
        self.filterStep = filterStep
        ni = alen(filter_width)
        self.classifier = bpnn.bpnn(ni, nh, nh_layer, no)
        self.filters = []
        for width in self.filterWidth:
            filter = [[int(random.uniform(-10, 10)) for j in range(vecLen)] for i in range(width)]
            self.filters.append(filter)

    def convolution(self, sentence, filter, step):
        featureMaps = []
        filter = array(filter)
        wordsArr = array(sentence)
        sentenceLen = wordsArr.shape[0]
        filterWidth = filter.shape[0]
        totalNum = int((sentenceLen - filterWidth) / step) + 1
        for i in range(totalNum):
            featureMaps.append(max(0, sum(filter * wordsArr[i:i + filterWidth])))  # use relu to active
        return featureMaps

    def maxPooling(self, featureMaps):
        return array(featureMaps).max()

    def classify(self, sentence):
        featureVec = []
        for filter in self.filters:
            featureMap = self.convolution(sentence, filter, self.filterStep)
            feature = self.maxPooling(featureMap)
            featureVec.append(feature)
        predictLabels = self.classifier.predict(featureVec)
        # classIdx = argsort(predictLabels)[-1]
        # return classIdx
        return predictLabels

    # the training set is the list of embedded sentence
    def train(self, trainingSet, labels, limit=10000, learn=0.05):
        featureVectors = []
        for sentence in trainingSet:
            featureVec = []
            for filter in self.filters:
                featureMaps = self.convolution(sentence, filter, self.filterStep)
                feature = self.maxPooling(featureMaps)
                featureVec.append(feature)
            featureVectors.append(featureVec)
        self.classifier.train(featureVectors, labels, limit, learn)


def testForEmail():
    docList = []
    classList = []
    for i in range(1, 26):
        wordList = one_hot.textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        classList.append([1])
        wordList = one_hot.textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        classList.append([0])
    vocabList = one_hot.createVocabList(docList)
    trainingSet = list(range(50))
    testSet = []
    for i in range(10):
        randIndex = int(random.uniform(0, alen(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del (trainingSet[randIndex])
    trainMat = []
    trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(one_hot.setOfWords2Mat(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    cnn = textCNN(alen(vocabList), [2, 3] * 50, 1, 50, 2, 1)
    cnn.train(trainMat, trainClasses)

    errorCounts = 0
    for docIndex in testSet:
        testDoc = one_hot.setOfWords2Mat(vocabList, docList[docIndex])
        returnedClass = cnn.classify(testDoc)
        print(returnedClass[0])
        returnedClass = 1 if returnedClass[0] >= 0.5 else 0
        print(classList[docIndex][0], " ", returnedClass)
        if returnedClass != classList[docIndex][0]:
            errorCounts += 1
    print('the error rate is:', float(errorCounts) / alen(testSet))
