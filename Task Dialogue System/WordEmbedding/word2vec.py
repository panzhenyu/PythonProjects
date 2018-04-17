# word2vec for word embedding
# panda

import gensim
import jieba
from gensim.models.word2vec import LineSentence


def preDeal(filename):
    src = open(filename)
    des = open(filename + ".preDeal", 'w')
    for doc in src.readlines():
        word_list = list(jieba.cut(doc.strip()))
        while ' ' in word_list:
            word_list.remove(' ')
        splitDoc = ' '.join(word_list)
        splitDoc += '\n'
        des.write(splitDoc)


def train(filename, outfile):
    print('start training word2vec')
    model = gensim.models.Word2Vec(LineSentence(filename), size=400, window=5, min_count=5)
    model.save(outfile)
    print('successfully trained')
    return model


def sentence2Mat(sentence, model):
    sentenceMat = []
    for word in sentence:
        if word in model:
            sentenceMat.append(model[word])
        else:
            sentenceMat.append([0] * model.vector_size)
            print("the word %s is not in my vocabulary" % word)
    return sentenceMat