# machine learning algorithm for rnn
# panda
# -*- coding: utf-8 -*-
from numpy import *


class rnn():
    @staticmethod
    def sigmoid(x):
        return 1 / (1 + exp(-x))

    @staticmethod
    def sigmoid_diff(x):
        sigX = rnn.sigmoid(x)
        return sigX * (1 - sigX)

    @staticmethod
    def Relu(x):
        return max(0, x)

    @staticmethod
    def Relu_diff(x):
        return 1 if x>0 else 0

    def __init__(self, input_dim, hidden_dim, output_dim):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim

        self.input_cell = list(2 * random.random(self.input_dim) - 1)
        self.hidden_cell = [0 * self.hidden_dim]
        self.output_cell = list(2 * random.random(self.output_dim) - 1)

        self.U = 2 * random.random((self.input_dim, self.hidden_dim)) - 1
        self.W = 2 * random.random((self.hidden_dim, self.hidden_dim)) - 1
        self.V = 2 * random.random((self.hidden_dim, self.output_dim)) - 1

    def train(self, sequence, iter_num=10000, alpha=0.1):
        pass