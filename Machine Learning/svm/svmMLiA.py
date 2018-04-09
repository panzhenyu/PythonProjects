# machine learning algorithm for svm
# panda
# -*- coding: utf-8 -*-
from numpy import *


# load data set from file
# the default separator is '\t'
# return lists of data and label
def loadDataSet(fileName, separator='\t'):
    dataList = []
    labelList = []
    fr = open(fileName)
    for line in fr.readlines():
        line = line.strip().split(separator)
        strData = line[0:len(line) - 1]
        floatData = map(lambda x: float(x), strData)
        dataList.append(floatData)
        labelList.append(float(line[-1]))
    return dataList, labelList


# choose another alpha
def selectJrand(i, m):
    j = i
    while (j == i):
        j = int(random.uniform(0, m))
    return j


# adjust alpha
def clipAlpha(aj, H, L):
    if aj > H:
        aj = H
    if aj < L:
        aj = L
    return aj


# algorithm of simplified SMO
def smoSimple(dataList, classLabels, C, tolerance, maxIter):
    dataMatrix = mat(dataList)
    labelMatrix = mat(classLabels).transpose()
    b = 0
    m, n = shape(dataMatrix)
    alphas = mat(zeros((m, 1)))
    iter = 0
    while iter < maxIter:
        alphaPairsChanged = 0
        for i in range(m):
            fXi = float(multiply(alphas, labelMatrix).T * (dataMatrix * dataMatrix[i].T)) + b
            Ei = fXi - float(labelMatrix[i])
            if ((labelMatrix[i] * Ei < -tolerance) and (alphas[i] < C)) or \
                    ((labelMatrix[i] * Ei > tolerance) and (alphas[i] > 0)):
                j = selectJrand(i, m)
                fXj = float(multiply(alphas, labelMatrix).T * (dataMatrix * dataMatrix[j].T)) + b
                Ej = fXj - float(labelMatrix[j])
                alphaIold = alphas[i].copy()
                alphaJold = alphas[j].copy()
                if labelMatrix[i] != labelMatrix[j]:
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])
                if L == H:
                    print("L == H")
                    continue
                eta = 2.0 * dataMatrix[i] * dataMatrix[j].T - \
                      dataMatrix[i] * dataMatrix[i].T - \
                      dataMatrix[j] * dataMatrix[j].T
                if eta >= 0:
                    print("eta >= 0")
                    continue
                alphas[j] -= labelMatrix[j] * (Ei - Ej) / eta
                alphas[j] = clipAlpha(alphas[j], H, L)
                if (abs(alphas[j] - alphaJold) < 0.00001):
                    print("j not moving enough")
                    continue
                alphas[i] += labelMatrix[j] * labelMatrix[i] * (alphaJold - alphas[j])
                b1 = b - Ei - \
                     labelMatrix[i] * (alphas[i] - alphaIold) * \
                     dataMatrix[i] * dataMatrix[i].T - \
                     labelMatrix[j] * (alphas[j] - alphaJold) * \
                     dataMatrix[i] * dataMatrix[j].T
                b2 = b - Ej - \
                     labelMatrix[i] * (alphas[i] - alphaIold) * \
                     dataMatrix[i] * dataMatrix[j].T - \
                     labelMatrix[j] * (alphas[j] - alphaJold) * \
                     dataMatrix[j] * dataMatrix[j].T
                if (0 < alphas[i]) and (C > alphas[i]):
                    b = b1
                elif (0 < alphas[j]) and (C > alphas[j]):
                    b = b2
                else:
                    b = (b1 + b2) / 2.0
                alphaPairsChanged += 1
                print("iter: %d i: %d, pairs changed %d" % (iter, i, alphaPairsChanged))
        if alphaPairsChanged == 0:
            iter += 1
        else:
            iter = 0
        print("iteration number: %d" % iter)
    return b, alphas


data, label = loadDataSet(r'testSet.txt')
b, alphas = smoSimple(data, label, 0.6, 0.001, 40)
print(b)
print(alphas)
