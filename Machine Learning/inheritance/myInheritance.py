# machine learning algorithm for inheritance
# panda
# made by self
# -*- coding: utf-8 -*-
from numpy import *


class Group:
    domain = []
    population = []
    fitness = 'null'
    bestFit = -inf
    bestInd = []
    worstFit = inf
    worstInd = []
    maxPop = 0
    def initPopulation(self, baseAmount):
        geneSize = len(self.domain)
        for i in range(baseAmount):
            ind = []
            for geneIndex in range(geneSize):
                gDomain = self.domain[geneIndex]
                ind.append(random.uniform(gDomain[0], gDomain[1]))
            self.population.append(ind)

    def encode(self):
        pass

    def decode(self):
        pass

    def evaluate(self):
        self.fitness = []
        for individual in self.population:
            self.fitness.append(self.fitFunc(individual))
        if max(self.fitness) > self.bestFit:
            self.bestFit = max(self.fitness)
            self.bestInd = self.population[self.fitness.index(self.bestFit)]
        if min(self.fitness) < self.worstFit:
            self.worstFit = min(self.fitness)
            self.worstInd = self.population[self.fitness.index(self.worstFit)]

    def select(self, selectRate):
        newPopulationIndex = []
        popAmount = len(self.population)
        selectAmount = selectRate * popAmount
        fitness = copy(self.fitness)
        indIndex = argsort(fitness)
        pi = sort(fitness) / sum(fitness)
        newPopulationIndex.append(indIndex[len(indIndex) - 1])
        while len(newPopulationIndex) < selectAmount:
            r = random.random()
            for index in range(len(pi)):
                r -= pi[index]
                if r <= 0:
                    break
            if index not in newPopulationIndex:
                newPopulationIndex.append(indIndex[index])
        newPopulation = []
        for i in newPopulationIndex:
            newPopulation.append(self.population[i])
        self.population = newPopulation

    def crossExchange(self, pCrossExchange):
        child = []
        for father in self.population:
            for mother in self.population:
                if len(self.population) + len(child) > self.maxPop:
                    self.population.extend(child)
                    return
                elif father != mother and random.random() < pCrossExchange:
                    if len(self.domain) == 1:
                        print("the amount of variable is too few")
                        exit()
                    r = int(random.uniform(1, len(self.domain) - 1))
                    c1 = list(copy(father))
                    c2 = list(copy(mother))
                    c1[r:], c2[r:] = c2[r:], c1[r:]
                    child.append(c1)
                    child.append(c2)
        self.population.extend(child)

    def mutation(self, pMutation, iterNum):
        child = []
        for i in range(len(self.population)):
            if len(self.population) + len(child) > self.maxPop:
                self.population.extend(child)
                return
            elif random.random() < pMutation:
                individual = list(copy(self.population[i]))
                gIdx = int(random.uniform(0, len(self.domain) - 1))
                gDomain = self.domain[gIdx]

                vk = individual[gIdx]
                ak = gDomain[0]
                bk = gDomain[1]
                T = (1 - self.fitFunc(individual)) / self.bestFit

                def h(t, y):
                    r = random.random()
                    return y * (1 - r ** (1 - t / iterNum) ** 2)

                newD1 = vk + h(T, bk - vk)
                newD2 = vk - h(T, vk - ak)
                individual[gIdx] = random.uniform(newD1, newD2)

                child.append(individual)
        self.population.extend(child)

    def fitFunc(self):
        pass

    def main(self, baseAmount, maxPop, variableDomain, selectRate, pCrossExchange, pMutation, iterNum, fitFunc):
        self.maxPop = maxPop
        self.domain = variableDomain
        self.initPopulation(baseAmount)
        self.fitFunc = fitFunc
        iter = 0
        while iter < iterNum:
            iter += 1
            self.evaluate()
            self.select(selectRate)
            self.crossExchange(pCrossExchange)
            self.mutation(pMutation, iterNum)
            print(iter, "th generator's best individual is: ", self.bestInd, "and it's fit is: ", self.bestFit)


g = Group()


def fit(ind):
    g = inf
    a1 = ind[0]
    w1 = ind[1]
    a2 = ind[2]
    w2 = ind[3]
    a3 = ind[4]
    w3 = ind[5]
    a4 = ind[6]
    w4 = ind[7]
    for i in arange(-10, 10, 0.1):
        for j in arange(-10, 10, 0.1):
            newg = (a1*w1*cos(w1*i)+a3*w3*cos(w3*i))**2 + (a2*w2*sin(w2*j)+a4*w4*sin(w4*j))**2
            if newg < g:
                if a1+a2+a3+a4 < 1 and a1+a2+a3+a4 > -1:
                    g = newg
                else:
                    return -newg
    return -g


g.main(20, 100, [(-100,100),(-100,100),(-100,100),(-100,100),(-100,100),(-100,100),(-100,100),(-100,100)], 0.5, 0.8, 0.1, 10, fit)
