""" roulete select utilities
"""
from random import uniform
from asyncga.numeric_individual import dejong_f1_individual
from xmlrpclib import MAXINT
from random import random
from asyncga.numeric_individual import dejong_f2_individual
import __main__

class roulete:
    def __init__(self, population, inverse=False):
        """initializes the roulete process
        """
        self.population = population
        fitnesses = [x.evaluate() for x in population]
        minf = min(fitnesses)
        # rescale fitnesses
        fitnesses = [x - minf for x in fitnesses]
        if inverse:
            maxf = max(fitnesses)
            fitnesses = [maxf - x for x in fitnesses]
        # now it's all between 0 and max
        self.fitnesses = fitnesses
        self.sumf = sum(fitnesses)
    def select(self):
        maxprob = uniform(0, self.sumf)
        current = 0
        acumm = 0
        while acumm < maxprob:
            acumm = acumm + self.fitnesses[current]
            current = current + 1
        return self.population[current-1]

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
        self.performance_calculator = performance_calculator()
    def run(self, maxiter, target=MAXINT, delta=0):
        """runs the GA
        """
        population = self.population
        best = population[0]
        best_eval = best.evaluate()
        iter = 0
        while iter < maxiter and abs(target - best_eval) > delta:
            selector = roulete(population, True)
            next_gen = [selector.select().mate(selector.select()) for i in range(0, self.size)]
            for individual in next_gen:
                if random() < self.mut_prob:
                    individual.mutate()
            best = get_best(next_gen)
            best_eval = best.evaluate()
            population = next_gen
            iter = iter + 1
            self.performance_calculator.update_iter([x.evaluate() for x in population])
            # printing is last thing
            print iter, best_eval, best, self.performance_calculator
        print iter, best_eval, best
        return best
    
def get_best(population):
    best = population[0]
    best_eval = best.evaluate()
    for individual in population:
        if individual.evaluate() < best_eval:
            best = individual
            best_eval = individual.evaluate()
    return best

class performance_calculator:
    """Calculates dejong's online and offline performances
    """
    def __init__(self):
        self.iter = 0
        self.online_sum = 0.0
        self.offline_sum = 0.0
    def update_iter(self, fitnesses):
        self.iter = self.iter + 1
        # online
        avg = 1.0*sum(fitnesses)/len(fitnesses)
        self.online_sum = self.online_sum + avg
        # offline
        bestfit = min(fitnesses)
        self.offline_sum = self.offline_sum + bestfit
    def online(self):
        return 1.0*self.online_sum/self.iter
    def offline(self):
        return 1.0*self.offline_sum/self.iter
    def __repr__(self):
        return "online: %f, offline %f" % (self.online(), self.offline())
    
class asyncga:
    def __init__(self, factory_method, size, life_expectancy=10):
        self.population = [factory_method() for i in range(0, size)]
        self.size = size
        self.life_expectancy = life_expectancy
        self.mut_prob = 0.01
        self.performance_calculator = performance_calculator()
    def run(self, maxiter, target=MAXINT, delta=0):
        population = self.population
        iter = 0
        best = get_best(population)
        best_eval = best.evaluate()
        while iter < maxiter and abs(target - best_eval) > delta:
            population = self.mate(population)
            population = self.mutate(population)
            population = self.die(population)
            best = get_best(population)
            best_eval = best.evaluate()
            self.population = population
            iter = iter + 1
            self.performance_calculator.update_iter([x.evaluate() for x in population])
            # printing is last thing
            print iter, len(self.population), best_eval, self.performance_calculator
        return best
    def mate(self, population):
        # mimics the traditional GA.
        selector = roulete(population, True)
        return [selector.select().mate(selector.select()) for i in range(0, self.size)]
    def mutate(self, population):
        for individual in population:
            if random() < self.mut_prob:
                individual.mutate()
        return population
    def die(self, population):
        # traditional GA, no one dies
        return population
        
class strategy1(asyncga):
    """implements some primitive type of mating and diying
    """
    def mate(self, population):
        """ 
        each "generation" gets (1/expectancy) more individuals
        so that population doubles over 1 lifetime and stabilizes
        on original size afterwards
        """
        selector = roulete(population, True)
        next_gen = [selector.select().mate(selector.select()) for i in range(0, self.size/self.life_expectancy)]
        return population + next_gen
    def die(self, population):
        [x.make_older() for x in population]
        return [x for x in population if x.get_age() <= self.life_expectancy]

if __main__:
    #ga = asyncga(lambda: dejong_f1_individual(), 200)
    ga = strategy1(lambda: dejong_f1_individual(), 200)
    ga.run(100, 0, 0.0001)
