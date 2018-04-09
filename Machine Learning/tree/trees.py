# machine learning algorithm for trees
# panda
# -*- coding: utf-8 -*-
from math import log
import operator


# create dataset
def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels


# convert file to dataset
def file2Vec(filename, separator='\t'):
    f = open(filename)
    contents = f.readlines()
    vec = []
    for str in contents:
        str = str.strip().split(separator)
        vec.append(str)
    return vec


# calculate shannonent of dataSet
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        labelCounts[currentLabel] = labelCounts.get(currentLabel, 0) + 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt


# divide dataset by value of feature
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis + 1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


# choose the best feature and return its index
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain, bestFeature = 0.0, -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain, bestFeature = infoGain, i
    return bestFeature


# return major class of a class list
def majorClass(classList):
    classCount = {}
    for vote in classList:
        classCount[vote] = classCount.get(vote, 0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


# create decision trees
def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorClass(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}
    del labels[bestFeat]
    fetValues = set([example[bestFeat] for example in dataSet])
    for values in fetValues:
        subLabels = labels[:]
        myTree[bestFeatLabel][values] = createTree(splitDataSet(dataSet, bestFeat, values), subLabels)
    return myTree


# use tree to classify
def classify(inputTree, featLabels, testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    FeatIndex = featLabels.index(firstStr)
    attr = testVec[FeatIndex]
    value = secondDict[attr]
    if isinstance(value, dict):
        return classify(value, featLabels, testVec)
    return value


# test based on lenses.txt
def LensesTest():
    dataSet = file2Vec(r'lenses.txt')
    print(dataSet)
    labels = ['f1', 'f2', 'f3', 'f4']
    tree = createTree(dataSet, labels)
    print(tree)


LensesTest()