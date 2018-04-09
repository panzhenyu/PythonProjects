# machine learning algorithm for logistics
# panda
# -*- coding: utf-8 -*-
from numpy import *


# load data from testSet.txt, return vector of data and label
def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open(r'testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat


# sigmoid
def sigmoid(inX):
        return 1.0 / (1 + exp(-inX))


# optimize weight by gradient ascent and return weights matrix
def gradAscent(dataMat, classLabels):
    dataMatrix = mat(dataMat)
    labelMat = mat(classLabels).transpose()
    m, n = shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500
    weights = ones((n, 1))
    for i in range(maxCycles):
        h = sigmoid(dataMatrix * weights)
        error = (labelMat - h)
        weights = weights + alpha * dataMatrix.transpose() * error
    return weights


# stochatic gradient ascent and return array of weights
def stocGradAscent(dataMatix, classLabels, numIter=150):
    m, n = shape(dataMatix)
    weights = ones(n)
    for j in range(numIter):
        dataIndex = list(range(m))
        for i in range(m):
            alpha = 4 / (1.0 + j + i) + 0.0001
            randIndex = int(random.uniform(0, alen(dataIndex)))
            h = sigmoid(sum(dataMatix[randIndex] * weights))
            error = classLabels[randIndex] - h
            weights = weights + alpha * error * array(dataMatix[randIndex])  # float cannot multiply list, thus, need to convert list to array
            del (dataIndex[randIndex])
    return weights


#use logistic to classify
def classifyVector(intX, weights):
    prob = sigmoid(sum(intX * weights))
    if prob > 0.5:
        return 1.0
    else:
        return 0.0


# plot decision edge
def plotBestFit(weight):
    import matplotlib.pyplot as plt
    weights = weight.getA()
    dataMat, labelMat = loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i, 1])
            ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1])
            ycord2.append(dataArr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)
    y = (-weights[0] - weights[1] * x) / weights[2]
    ax.plot(x, y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()


# test logistics based on horseColicTest.txt and horseColicTraining.txt
def colicTest():
    frTrain = open(r'horseColicTraining.txt')
    frTest = open(r'horseColicTest.txt')
    trainingSet = []
    trainingLabels = []
    for line in frTrain.readlines():
        data = line.strip().split('\t')
        training = list(map(lambda x: float(x), data))
        trainingSet.append(training[0:alen(training) - 1])
        trainingLabels.append(training[-1])
    testSet = []
    testLabels = []
    for line in frTest.readlines():
        data = line.strip().split('\t')
        test = list(map(lambda x: float(x), data))
        testSet.append(test[0:alen(test) - 1])
        testLabels.append(test[-1])
    weights = array(stocGradAscent(trainingSet, trainingLabels, 150))
    errorCounts = 0
    for i in range(alen(testSet)):
        vec = testSet[i]
        classifyResult = classifyVector(vec, weights)
        if classifyResult != testLabels[i]:
            errorCounts += 1
    print("the error rate is: ", float(errorCounts) / alen(testSet))

data, labels = loadDataSet()
weights = mat(stocGradAscent(data, labels))
plotBestFit(weights.T)
