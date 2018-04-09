# bpnn needs 4 parameters : input_num, hidden_num, hiddenLayer_num, output_num

from numpy import *


def sigmoid(x):
    return 1 / (1 + exp(-x))


def differential_sigmoid(x):
    y = sigmoid(x)
    return y * (1 - y)


def rand(a, b):
    return random.uniform(a, b)


def softMax(output_cells):
    output = array(output_cells)
    return list(exp(output) / sum(exp(output)))


def differential_softMax(output_cells):
    output_cells = array(softMax(output_cells))
    return list(output_cells * (1 - output_cells))


class bpnn:
    def __init__(self, input_num, hidden_num, hiddenLayer_num, output_num):
        self.input_num = input_num + 1
        self.hidden_num = hidden_num
        self.hiddenLayer_num = hiddenLayer_num
        self.output_num = output_num
        self.weight_num = hiddenLayer_num + 1

        self.weights = []
        weight = [[rand(-0.2, 0.2) for j in range(self.hidden_num)] for i in range(self.input_num)]
        self.weights.append(weight)
        for i in range(self.weight_num - 2):
            self.weights.append([[rand(-0.2, 0.2) for j in range(self.hidden_num)] for i in range(self.hidden_num)])
        self.weights.append([[rand(-0.2, 0.2) for j in range(self.output_num)] for i in range(self.hidden_num)])

        self.input_cells = [1.0] * self.input_num
        self.hidden_cells = [[1.0] * self.hidden_num] * self.hiddenLayer_num
        self.output_cells = [1.0] * self.output_num

    def predict(self, case):
        for i in range(self.input_num - 1):
            self.input_cells[i] = case[i]

        weight = array(self.weights[0]).T
        self.hidden_cells[0] = [sigmoid(x) for x in list((weight * self.input_cells).sum(1))]
        for i in range(1, self.hiddenLayer_num):
            weight = array(self.weights[i]).T
            self.hidden_cells[i] = [sigmoid(x) for x in list((weight * self.hidden_cells[i - 1]).sum(1))]

        weight = array(self.weights[-1]).T
        self.output_cells = [sigmoid(x) for x in list((weight * self.hidden_cells[-1]).sum(1))]

        return list(self.output_cells)

    def back_propagate(self, case, label, learn):
        self.predict(case)

        output_deltas = [0.0] * self.output_num
        for o in range(self.output_num):
            error = label[o] - self.output_cells[o]
            output_deltas[o] = error * differential_sigmoid(self.output_cells[o])

        hidden_deltas = [[0.0] * self.hidden_num] * self.hiddenLayer_num
        error = list((array(self.weights[-1]) * output_deltas).sum(1))
        for h in range(self.hidden_num):
            hidden_deltas[-1][h] = error[h] * differential_sigmoid(self.hidden_cells[-1][h])
        i = -2
        while i >= -self.hiddenLayer_num:
            error = (array(self.weights[i]) * hidden_deltas[i + 1]).sum(1)
            for h in range(self.hidden_num):
                hidden_deltas[i][h] = error[h] * differential_sigmoid(self.hidden_cells[i][h])
            i -= 1

        weightMat = array(self.weights[-1])
        changeMat = array(mat(self.hidden_cells[-1]).T * output_deltas)
        for h in range(self.hidden_num):
            weightMat[h] += learn * changeMat[h]
        self.weights[-1] = list(weightMat)
        i = -2
        while i >= -self.hiddenLayer_num:
            weightMat = array(self.weights[i])
            changeMat = array(mat(self.hidden_cells[i]).T * hidden_deltas[i + 1])
            for h in range(self.hidden_num):
                weightMat[h] -= learn * changeMat[h]
            self.weights[i] = list(weightMat)
            i -= 1
        weightMat = array(self.weights[0])
        changeMat = array(mat(self.input_cells).T * hidden_deltas[0])
        for i in range(self.input_num):
            weightMat[i] += learn * changeMat[i]
        self.weights[0] = list(weightMat)

        error = 0.0
        for o in range(len(label)):
            error += 0.5 * (label[o] - self.output_cells[o]) ** 2
        return error

    def train(self, cases, labels, limit=10000, learn=0.05):
        for j in range(limit):
            error = 0.0
            for i in range(len(cases)):
                label = labels[i]
                case = cases[i]
                error += self.back_propagate(case, label, learn)
            print("the", j, "th error is", error)

    def test(self):
        cases = [[-1, -1], [-2, -1], [1, 3], [1, 1]]
        labels = [[0, 1], [0, 1], [1, 0], [1, 0]]
        self.train(cases, labels)
        cases.append([5, 5])
        for case in cases:
            print(self.predict(case))
