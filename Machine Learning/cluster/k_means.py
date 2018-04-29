# machine learning algorithm for k-means
# panda
# -*- coding: utf-8 -*-
from numpy import *
import matplotlib.pyplot as plt

# return data matrix
def loadDataMat(filename):
    dataMat = []
    fp = open(filename)
    for info in fp.readlines():
        dataMat.append([float(x) for x in info.strip().split("\t")])
    return mat(dataMat)


def distEclud(vec1, vec2):
    return sqrt(power(vec1 - vec2, 2).sum())


def calc_center(category):
    pass


# return center matrix
def randCent(dataMat, k):
    n = shape(dataMat)[1]
    centroids = mat(zeros((k, n)))
    for j in range(n):
        minJ = dataMat[:, j].min()
        rangeJ = dataMat[:, j].max() - minJ
        centroids[:, j] = minJ + rangeJ * random.rand(k, 1)
    return centroids


# kernel algorithm for k-means
def kMeans(dataMat, k, distMeas=distEclud, createCent=randCent):
    m = dataMat.shape[0]
    clusterAssment = mat(zeros((m,2)))
    centroids = createCent(dataMat, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = inf
            minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j, :], dataMat[i, :])
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            if clusterAssment[i,0] != minIndex:
                clusterChanged = True
                clusterAssment[i, :] = minIndex, minDist**2
        for cent in range(k):
            ptsInClust = dataMat[nonzero(clusterAssment[:, 0].A==cent)[0]]
            centroids[cent, :] = mean(ptsInClust, axis=0)
    return centroids, clusterAssment


dataMat = loadDataMat(r'testSet.txt')
centroids, cluster = kMeans(dataMat, 3)

colorMap = {0:'red', 1:'green', 2:'black', 3:'blue', 4:"yellow", 5:"magenta"}
fig = plt.figure()
for i in range(dataMat.shape[0]):
    plt.scatter(dataMat[i,0], dataMat[i,1], color=colorMap[int(cluster[i,0])])
for i in range(centroids.shape[0]):
    plt.scatter(centroids[i,0], centroids[i,1], s=500, color=colorMap[i], marker='+')
fig.show()