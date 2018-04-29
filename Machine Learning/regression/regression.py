# machine learning algorithm for regression
# panda
# -*- coding: utf-8 -*-
from numpy import *
import matplotlib.pyplot as plt


def loadDataset(filename, separator='\t'):
    fp = open(filename)
    dataList = []
    labelList = []
    for line in fp.readlines():
        line = line.strip().split(separator)
        numLine = map(lambda x: float(x), line)
        dataList.append(numLine[0:len(line) - 1])
        labelList.append(numLine[-1])
    return dataList, labelList


# the following two regressions need that the feature matrix isn't a singular matrix
def standRegres(xArr, yArr):
    xMat = mat(xArr)
    yMat = mat(yArr).T
    xTx = xMat.T * xMat
    if linalg.det(xTx) == 0:
        print("the matrix is singular")
        return
    w = xTx.I * xMat.T * yMat
    return w


def ex0Test_standRegress():
    data, labels = loadDataset(r'ex0.txt')
    w = standRegres(data, labels)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(mat(data)[:, 1].flatten().A[0], array(labels))
    xCopy = mat(data).copy()
    yHat = xCopy * w
    ax.plot(xCopy[:, 1], yHat)
    plt.show()


def lwlr(testPoint, xArr, yArr, k=1.0):
    xMat = mat(xArr)
    yMat = mat(yArr).T
    m = shape(xMat)[0]
    weights = mat(eye(m))
    for j in range(m):
        diffMat = testPoint - xMat[j]
        weights[j, j] = exp(diffMat * diffMat.T / (-2.0 * k ** 2))
    xTx = xMat.T * (weights * xMat)
    if linalg.det(xTx) == 0.0:
        print("the matrix is singular")
        return
    ws = xTx.I * xMat.T * weights * yMat
    return testPoint * ws


def lwlrTest(testArr, xArr, yArr, k=1.0):
    m = shape(testArr)[0]
    yHat = zeros(m)
    for i in range(m):
        yHat[i] = lwlr(testArr[i], xArr, yArr, k)
    return yHat


def ex0Test_lwlr():
    data, labels = loadDataset(r'ex0.txt')
    yHat = lwlrTest(data, data, labels, 0.01)
    xMat = mat(data)
    srtInd = xMat[:, 1].argsort(0)
    xSort = data[srtInd]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(xSort[:, 1], yHat[srtInd])
    ax.scatter(xMat[:, 1].flatten().A[0], mat(yHat).T.flatten().A[0])
    plt.show()
