""" roulete select utilities
"""
from random import uniform
from asyncga.numeric_individual import dejong_f1_individual
from xmlrpclib import MAXINT
from random import random
from asyncga.numeric_individual import dejong_f2_individual
import __main__

def roulete_select(population, inverse = False):
    """roulete selects in a population
    """
    fitnesses = [x.evaluate() for x in population]
    minf = min(fitnesses)
    # rescale fitnesses
    fitnesses = [x - minf for x in fitnesses]
    if inverse:
        maxf = max(fitnesses)
        fitnesses = [maxf - x for x in fitnesses]
    # now it's all between 0 and max
    sumf = sum(fitnesses)
    maxprob = uniform(0, sumf)
    current = 0
    acumm = 0
    while acumm < maxprob:
        acumm = acumm + fitnesses[current]
        current = current + 1
    return population[current-1]

class traditional_ga:
    """This class implements the traditional ga.
    1 - creates a static sized population
    2 - aplies the defined probabilities in order to create a new pop
    3 - until some good result is obtained or max iterations is atained
    """
    def __init__(self, factory_method, size):
        self.population = [factory_method() for i in range(0, size)]
        self.size = size
        self.mut_prob = 0.01
    def run(self, maxiter, target=MAXINT, delta=0):
        """runs the GA
        """
        population = self.population
        best = population[0]
        best_eval = best.evaluate()
        iter = 0
        while iter < maxiter and abs(target - best_eval) > delta:
            next_gen = [roulete_select(population, True).mate(roulete_select(population, True)) for i in range(0, self.size)]
            for individual in next_gen:
                if random() < self.mut_prob:
                    individual.mutate()
            best = next_gen[0]
            best_eval = best.evaluate()
            for individual in next_gen:
                if individual.evaluate() < best_eval:
                    best = individual
                    best_eval = individual.evaluate()
            population = next_gen
            print iter, best_eval, best
            iter = iter + 1
        print iter, best_eval, best
        return best
        

if __main__:
    ga = traditional_ga(lambda: dejong_f2_individual(), 1000)
    ga.run(100, 0, 0.001)
