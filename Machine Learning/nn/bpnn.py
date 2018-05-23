# machine learning algorithm for bpnn
# panda
# -*- coding: utf-8 -*-
from numpy import *


class bpnn:

    def rand(self, a, b):
        return (b - a) * random.random() + a

    def make_matrix(self, m, n, fill=0.0):
        mat = []
        for i in range(m):
            mat.append([fill] * n)
        return mat

    def sigmoid(self, x):
        return 1.0 / (1.0 + exp(-x))

    def sigmoid_derivative(self, x):
        x = self.sigmoid(x)
        return x * (1 - x)

    def setup(self, ni, nh, no):
        self.input_n = ni + 1
        self.hidden_n = nh
        self.output_n = no

        self.input_cells = [1.0] * self.input_n
        self.hidden_cells = [1.0] * self.hidden_n
        self.output_cells = [1.0] * self.output_n

        self.input_weights = self.make_matrix(self.input_n, self.hidden_n)
        self.output_weights = self.make_matrix(self.hidden_n, self.output_n)

        for i in range(self.input_n):
            for h in range(self.hidden_n):
                self.input_weights[i][h] = self.rand(-0.2, 0.2)
        for h in range(self.hidden_n):
            for o in range(self.output_n):
                self.output_weights[h][0] = self.rand(-0.2, 0.2)

        self.input_correction = self.make_matrix(self.input_n, self.hidden_n)
        self.output_correction = self.make_matrix(self.hidden_n, self.output_n)

    def predict(self, inputs):
        for i in range(self.input_n - 1):
            self.input_cells[i] = inputs[i]

        _hidden_cells = multiply(array(self.input_cells), array(self.input_weights).T).sum(1)
        self.hidden_cells = [self.sigmoid(x) for x in _hidden_cells]

        _output_cells = multiply(array(self.hidden_cells), array(self.output_weights).T).sum(1)
        self.output_cells = [self.sigmoid(x) for x in _output_cells]
        return list(self.output_cells)

    def back_propagate(self, case, label, learn, correct):
        self.predict(case)

        output_deltas = [0.0] * self.output_n
        for o in range(self.output_n):
            error = label[o] - self.output_cells[o]
            output_deltas[o] = error * self.sigmoid_derivative(self.output_cells[o])

        hidden_deltas = [0.0] * self.hidden_n
        error = list((output_deltas * array(self.output_weights)).sum(1))
        for h in range(self.hidden_n):
            # error = 0
            # for o in range(self.output_n):
            #     error += output_deltas[o] * self.output_weights[h][o]
            hidden_deltas[h] = error[h] * self.sigmoid_derivative(self.hidden_cells[h])

        changeMat = array(mat(self.hidden_cells).T * output_deltas)
        for h in range(self.hidden_n):
            self.output_weights[h] += learn * changeMat[h]
        # for h in range(self.hidden_n):
        #     for o in range(self.output_n):
        #         change = output_deltas[o] * self.hidden_cells[h]
        #         self.output_weights[h][o] += learn * change + correct * self.output_correction[h][o]
        #         self.output_correction[h][o] = change
        changeMat = array(mat(self.input_cells).T * hidden_deltas)
        for i in range(self.input_n):
            self.input_weights += learn * changeMat[i]
        # for i in range(self.input_n):
        #     for h in range(self.hidden_n):
        #         change = hidden_deltas[h] * self.input_cells[i]
        #         self.input_weights[i][h] += learn * change + correct * self.input_correction[i][h]
        #         self.input_correction[i][h] = change

        error = 0.0
        for o in range(alen(label)):
            error += 0.5 * (label[o] - self.output_cells[o]) ** 2

        return error

    def train(self, cases, labels, limit=10000, learn=0.05, correct=0.1):
        for j in range(limit):
            error = 0.0
            for i in range(alen(cases)):
                label = labels[i]
                case = cases[i]
                error += self.back_propagate(case, label, learn, correct)
            print("the", j, "th error is", error)

    def test(self):
        cases = [[-1, -1], [-2, -1], [1, 3], [1, 1]]
        labels = [[0, 1], [0, 1], [1, 0], [1, 0]]
        self.setup(2, 5, 2)
        self.train(cases, labels)
        cases.append([5, 5])
        for case in cases:
            print(self.predict(case))

    def testFortestSet(self):
        cases = []
        labels = []
        fp = open(r'/home/panda/MLDatas/testSet.txt')
        for line in fp.readlines():
            line = line.strip().split('\t')
            x_arr = [float(x) for x in line[0:2]]
            cases.append(x_arr)
            if float(line[-1]) == -1:
                labels.append([1])
            else:
                labels.append([0])
        self.setup(2, 5, 1)
        self.train(cases, labels, 2000)
        sampleNum = len(cases)
        sampleIndex = range(len(cases))
        trainSet = []
        testSet = []
        while (len(sampleIndex) > sampleNum / 5):
            randIdx = int(random.uniform(0, len(sampleIndex)))
            trainSet.append(sampleIndex[randIdx])
            del (sampleIndex[randIdx])
        while (len(sampleIndex) > 0):
            testSet.append(sampleIndex[0])
            del (sampleIndex[0])

        self.train(array(cases)[trainSet], array(labels)[trainSet], 10000, 0.01)
        errorNum = 0.0
        for testIdx in testSet:
            testSample = cases[testIdx]
            realLabel = labels[testIdx]
            predictLabel = self.predict(testSample)
            predictLabel[0] = 1 if predictLabel[0] > 0.5 else 0
            if realLabel[0] != predictLabel[0]:
                errorNum += 1
                print("sample:", testSample, "realLabel:", realLabel, "predictLabel:", predictLabel)
        print("test error rate:", errorNum / len(testSet))

        errorNum = 0.0
        for testIdx in trainSet:
            testSample = cases[testIdx]
            realLabel = labels[testIdx]
            predictLabel = self.predict(testSample)
            predictLabel[0] = 1 if predictLabel[0] > 0.5 else 0
            if realLabel[0] != predictLabel[0]:
                errorNum += 1
                print("sample:", testSample, "realLabel:", realLabel, "predictLabel:", predictLabel)
        print("train error rate:", errorNum / len(trainSet))


b1 = bpnn()
b1.test()
