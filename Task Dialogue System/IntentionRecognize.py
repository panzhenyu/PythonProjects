# intention recognition needs to set prepared intentions
# this classifier is based on neural network
# classifier returns a most possible class

import jieba
from NeutralNetwork import textCNN
from WordEmbedding import one_hot
from WordEmbedding import word2vec
import gensim
from numpy import *


# return data list
def loadDataSet(filename):
    data = []
    label = []
    fp = open(filename, encoding='utf-8', errors='ignore')
    for sentence in fp.readlines():
        sentence = list(jieba.cut(sentence.strip('[。，,.;\n]')))
        data.append(sentence)
        label.append(filename[filename.find('_') + 1:filename.find('.')])
    return data, label


def training(dataMat, labels, filter, step, nh, num_h, limits=10000, learn=0.05):
    vecLen = alen(dataMat[0][0])
    classLen = alen(labels[0])
    classifier = textCNN.textCNN(vecLen, filter, step, nh, num_h, classLen)
    classifier.train(dataMat, labels, limits, learn)
    return classifier


def test():
    data, label = loadDataSet(r'/home/panda/MLDatas/train_flight.txt')
    t_data, t_label = loadDataSet(r'/home/panda/MLDatas/train_train.txt')
    data.extend(t_data)
    label.extend(t_label)
    label = one_hot.sentence2Mat(list(set(label)), label)
    dataMat = []
    model = gensim.models.Word2Vec.load('Models/mix.model-word2vec')
    for sentence in data:
        dataMat.append(word2vec.sentence2Mat(sentence, model))

    data_num = alen(dataMat)
    training_idx = []
    test_idx = list(range(data_num))
    for i in range(int(data_num / 10)):
        randIdx = random.random_integers(0, alen(test_idx) - 1)
        training_idx.append(test_idx[randIdx])
        del (test_idx[randIdx])
    trainingData = [dataMat[idx] for idx in training_idx]
    trainingLabel = [label[idx] for idx in training_idx]

    classifier = training(trainingData, trainingLabel, [1, 2] * 30, 1, 15, 1, 10000)
    error = 0.0
    for testSentenceIdx in test_idx:
        predictLabel = classifier.classify(dataMat[testSentenceIdx])
        if argsort(predictLabel)[-1] != argsort(label[testSentenceIdx])[-1]:
            print(data[testSentenceIdx], " ", predictLabel, " ", label[testSentenceIdx])
            error += 1
    print("error rate:", error / alen(test_idx))

test()