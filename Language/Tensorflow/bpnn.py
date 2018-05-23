import tensorflow as tf
import numpy

class bpnn:
    def __init__(self, ni, nh, no):
        self.ni = ni
        self.nh = nh
        self.no = no

        self.W_ih = tf.Variable(tf.random_normal([self.nh, self.ni], stddev=1, seed=1))
        self.W_ho = tf.Variable(tf.random_normal([self.no, self.nh], stddev=1, seed=1))

        self.input_layer = tf.placeholder(tf.float32, [self.ni, None])
        self.hidden_layer = tf.nn.sigmoid(tf.matmul(self.W_ih, self.input_layer))
        self.output_layer = tf.nn.sigmoid(tf.matmul(self.W_ho, self.hidden_layer))

        init = tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(init)

    def predict(self, data):
        data = numpy.mat(data).T
        return self.sess.run(self.output_layer, {self.input_layer: data})

    def train(self, trainingSet, labels, limit=10000):
        y = tf.placeholder(tf.float32, [self.no, None])
        loss = tf.reduce_mean(tf.square(self.output_layer - y))
        trainer = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

        amount = len(trainingSet)
        for _ in range(limit):
            for i in range(amount-1):
                data = numpy.mat(trainingSet[i:i+2]).T
                label = numpy.mat(labels[i:i+2])
                self.sess.run(trainer, {self.input_layer: data, y: label})
            print(_)

# fp = open(r'/home/panda/MLDatas/testSet.txt')
# dataSet = []
# labels = []
# for line in fp.readlines():
#     line = list(map(float, line.strip().split('\t')))
#     dataSet.append(line[0: len(line)-1])
#     if line[-1] == -1:
#         labels.append([1,0])
#     else:
#         labels.append([0,1])
#
# num = len(dataSet)
# trainingSet = list(range(num))
# testSet = []
# for _ in range(num // 5):
#     r = int(numpy.random.uniform(0, len(trainingSet)))
#     testSet.append(trainingSet[r])
#     del(trainingSet[r])
# classifier = bpnn(len(dataSet[0]), 3, len(labels[0]))
# classifier.train([dataSet[i] for i in trainingSet], [labels[i] for i in trainingSet])

# cases = [[-1, -1], [-2, -1], [1, 3], [1, 1]]
# labels = [[0, 1], [0, 1], [1, 0], [1, 0]]
# classifier = bpnn(len(cases[0]), 5, len(labels[0]))
# classifier.train(cases, labels)
# for case in cases:
#     print(classifier.predict(case))

# for i in range(num // 4):
#     print(classifier.predict(dataSet[testSet[i]]), labels[i])

# input_layer = tf.placeholder(tf.float32,[1, 4])
# W_ih = tf.Variable(tf.random_uniform((4,1), -0.2, 0.2, dtype=tf.float32), dtype=tf.float32)
# y = tf.matmul(W_ih, input_layer)
# init = tf.global_variables_initializer()
#
# sess = tf.Session()
# sess.run(init)
# x = sess.run(input_layer, {input_layer: numpy.mat([1,2,3,4])})
# print(x)
# print(sess.run(y, {input_layer: x}))

i = tf.Variable(tf.random_normal((1,2), ))
sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init)
print(sess.run(i))