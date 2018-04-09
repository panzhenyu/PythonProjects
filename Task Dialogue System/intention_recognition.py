# intention recognition needs to set prepared intentions
# this classifier is based on neural network
# classifier returns a most possible class

import jieba
from NeutralNetwork import textCNN
from TextProcession import one_hot
from numpy import *


# return data list
def loadDataSet(filename):
    data = []
    label = []
    fp = open(filename, encoding='utf-8')
    for sentence in fp.readlines():
        sentence = list(jieba.cut(sentence.strip('[。，,.;\n]')))
        data.append(sentence)
        label.append(filename[filename.find('_') + 1:filename.find('.')])
    return data, label


def getVocabulary(data):
    return one_hot.createVocabList(data)


def data2Mat(data):
    vocabulary = getVocabulary(data)
    dataMat = []
    for sentence in data:
        sentenceMat = one_hot.setOfWords2Mat(vocabulary, sentence)
        dataMat.append(sentenceMat)
    return dataMat


def training(dataMat, labels, filter, step, nh, num_h, limits=10000, learn=0.05):
    vecLen = shape(dataMat[0])[1]
    classLen = alen(labels[0])
    classifier = textCNN.textCNN(vecLen, filter, step, nh, num_h, classLen)
    classifier.train(dataMat, labels, limits, learn)
    return classifier


def test():
    data, label = loadDataSet(r'train_flight.txt')
    t_data, t_label = loadDataSet(r'train_train.txt')
    data.extend(t_data)
    label.extend(t_label)
    label = one_hot.setOfWords2Mat(list(set(label)), label)
    dataMat = data2Mat(data)
    data_num = alen(dataMat)
    training_idx = []
    test_idx = list(range(data_num))
    for i in range(int(data_num / 5)):
        randIdx = random.random_integers(0, alen(test_idx) - 1)
        training_idx.append(test_idx[randIdx])
        del (test_idx[randIdx])
    trainingData = [dataMat[idx] for idx in training_idx]
    trainingLabel = [label[idx] for idx in training_idx]

    classifier = training(trainingData, trainingLabel, [1] * 50, 1, 20, 1, 10000)
    error = 0.0
    for testSentenceIdx in test_idx:
        predictLabel = classifier.classify(dataMat[testSentenceIdx])
        if argsort(predictLabel)[-1] != argsort(label[testSentenceIdx])[-1]:
            print(data[testSentenceIdx], " ", predictLabel, " ", label[testSentenceIdx])
            error += 1
    print("error rate:", error / alen(test_idx))


test()
