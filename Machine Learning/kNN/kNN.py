# machine learning algorithm for kNN
# panda
# -*- coding: utf-8 -*-
from numpy import *
import operator
from os import listdir


# test dataset
def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


# convert file to matrix , needs filename and separator
# file content pattern : feature1 feature2 ...label
# default separator is \t
# return the matrix of feature and vector of label
def file2matrix(filename, separator='\t'):
    fr = open(filename)
    arrayOfLines = fr.readlines()
    numberOfLines = len(arrayOfLines)
    numberOfFeature = len(arrayOfLines[0].strip().split(separator)) - 1
    returnMat = zeros((numberOfLines, numberOfFeature))
    classLabelVector = []
    index = 0
    for line in arrayOfLines:
        line = line.strip()
        listFromLine = line.split(separator)
        returnMat[index, :] = listFromLine[0:numberOfFeature]
        classLabelVector.append(listFromLine[-1])
        index += 1
    return returnMat, classLabelVector


# convert imagine to vector
# default size : 1 1024
def img2vector(filename):
    fr = open(filename)
    returnVec = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVec[0, 32 * i + j] = int(lineStr[j])
    return returnVec


# the formula : (olddata-min)/(max-min)
# give the original dataSet, return the normalized dataMat
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    row = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (row, 1))
    normDataSet = normDataSet / tile(ranges, (row, 1))
    return normDataSet, ranges, minVals


# kernal code
def kNN(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** 0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


# test based on trainingDigits and testDigits
def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir(r'trainingDigits')
    trainingSize = len(trainingFileList)
    trainingMat = zeros((trainingSize, 1024))
    for i in range(trainingSize):
        filename = trainingFileList[i]
        trainingVector = img2vector(r'trainingDigits/' + filename)
        hwLabels.append(int(filename[0]))
        trainingMat[i, :] = trainingVector
    testFileList = listdir(r'testDigits')
    errorCount = 0.0
    testSize = len(testFileList)
    for i in range(testSize):
        filename = testFileList[i]
        testVector = img2vector(r'testDigits/' + filename)
        realLabel = int(filename[0])
        result = kNN(testVector, trainingMat, hwLabels, 20)
        print("the hand writing classifier came back with: %s, the real answer is: %s" % (result, realLabel))
        if result != realLabel:
            errorCount += 1.0
    print("\n the total number of errors is: %d" % errorCount)
    print("\n the error rate is: %f" % (errorCount / testSize))


# test based on datingTestSet.txt
def datingClassTest():
    hoRatio = 0.1
    datingDataMat, datingLabels = file2matrix(r'datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    numTestVecs = int(normMat.shape[0] * hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = kNN(normMat[i], normMat[numTestVecs:], datingLabels[numTestVecs:], 3)
        print("the kNN came back with: %s, the real answer is: %s" % (classifierResult, datingLabels[i]))
        if classifierResult != datingLabels[i]:
            errorCount += 1.0
    print("the total error rate is: %f" % (errorCount / numTestVecs))


# interacitve using , the dataSet is based on datingTestSet.txt
def classifyPerson():
    percentTats = float(input("percentage of time spent playing video games?"))
    ffMiles = float(input("frequent flier miles earned per year?"))
    iceCream = float(input("liters of ice cream consumed per year"))
    datingDataMat, datingLabels = file2matrix(r'datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    classifyResult = kNN(array([ffMiles, percentTats, iceCream]), normMat, datingLabels, 3)
    print("You will probably like this person: %s" % classifyResult)


handwritingClassTest()
