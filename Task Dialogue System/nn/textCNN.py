# cnn for text classification
# panda
# -*- coding: utf-8 -*-
from numpy import *
from nn import bpnn


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
