""" roulete select utilities
"""
from random import uniform
from asyncga.numeric_individual import dejong_f1_individual
from xmlrpclib import MAXINT
from random import random
from asyncga.numeric_individual import dejong_f2_individual
from random import normalvariate
from asyncga.numeric_individual import dejong_f3_individual
from asyncga.numeric_individual import dejong_f4_individual
from asyncga.numeric_individual import dejong_f5_individual
import sys
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
        self.online_last = 0.0
        self.offline_sum = 0.0
    def update_iter(self, fitnesses):
        self.iter = self.iter + 1
        # online
        avg = 1.0*sum(fitnesses)/len(fitnesses)
        self.online_sum = self.online_sum + avg
        self.online_last = avg
        # offline
        bestfit = min(fitnesses)
        self.offline_sum = self.offline_sum + bestfit
    def online1(self):
        return 1.0*self.online_sum/self.iter
    def online2(self):
        return self.online_last
    def offline(self):
        return 1.0*self.offline_sum/self.iter
    def __repr__(self):
        return "online1: %f, online2: %f, offline %f" % (self.online1(), self.online2(), self.offline())
    
class asyncga:
    def __init__(self, factory_method, size, life_expectancy=10, stats=None):
        self.population = [factory_method() for i in range(0, size)]
        self.size = size
        self.life_expectancy = life_expectancy
        self.mut_prob = 0.01
        self.performance_calculator = performance_calculator()
        self.stats = stats
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
            if self.stats:
                self.stats.colect("a-len", iter, len(self.population))
                self.stats.colect("b-best", iter, best_eval)
                self.stats.colect("c-online1", iter, self.performance_calculator.online1())
                self.stats.colect("d-online2", iter, self.performance_calculator.online2())
                self.stats.colect("e-offline", iter, self.performance_calculator.offline())
            else:
                print iter, len(self.population), best_eval, self.performance_calculator
        #print self.stats
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
        ret = [x for x in population if x.get_age() <= self.life_expectancy]
        if len(ret) <= 0:
            selector = roulete(population, True)
            ret = [selector.select(), selector.select()]
        return ret

class strategy2(strategy1):
    """
    Adjusts dying age acording to fitness
    """
    def die(self, population):
        """
        most fit die old, less fit die young
        """
        [x.make_older() for x in population]
        fitnesses = [x.evaluate() for x in population]
        minf = min(fitnesses)
        # rescale fitnesses
        fitnesses = [x - minf for x in fitnesses]
        maxf = max(fitnesses)
        # normalize
        if maxf * self.life_expectancy > 1:
            fitnesses = [1-(x/maxf) for x in fitnesses]
        else:
            return population
        ages = [x.get_age() for x in population]
        #print [(ages[i], fitnesses[i], fitnesses[i] * self.life_expectancy) for i in range(0, len(ages))]
        ret = [population[i] for i in range(0, len(population)) if ages[i] <= self.life_expectancy * fitnesses[i]]
        if len(ret) < 1:
            selector = roulete(population, True)
            ret = [selector.select()]
        return ret

class strategy3(strategy2):
    """
    stochastic number of breadings
    """
    def mate(self, population):
        """ 
        number of new individuas per generation is a normal distribution
        with N/life_expectancy as mean and N/2 as stddev.
        """
        num = normalvariate(self.size/self.life_expectancy, self.size/(2.0*self.life_expectancy))
        #print "num:", num
        selector = roulete(population, True)
        next_gen = [selector.select().mate(selector.select()) for i in range(0, num)]
        return population + next_gen
    
class strategy4(strategy3):
    """
    stochastic deaths
    """
    def die(self, population):
        """
        deaths are adjusted by fitness and by a random normal distributed factor.
        I'll try normal(life_expectancy * fitnesses, life_expectancy/2)
        """
        [x.make_older() for x in population]
        fitnesses = [x.evaluate() for x in population]
        minf = min(fitnesses)
        # rescale fitnesses
        fitnesses = [x - minf for x in fitnesses]
        maxf = max(fitnesses)
        # normalize
        if maxf * self.life_expectancy > 1:
            fitnesses = [1-(x/maxf) for x in fitnesses]
        else:
            return population
        ages = [x.get_age() for x in population]
        #print [(ages[i], fitnesses[i], fitnesses[i] * self.life_expectancy) for i in range(0, len(ages))]
        stochastic_ages = [normalvariate(self.life_expectancy * fitnesses[i], self.life_expectancy/2.0) for i in range(0, len(population))]
        ret = [population[i] for i in range(0, len(population)) if ages[i] <= stochastic_ages[i]]
        if len(ret) < 1:
            selector = roulete(population, True)
            ret = [selector.select()]
        return ret
    
class stats_colector:
    """
    Colects stats and prints them as CSV
    """
    def __init__(self):
        self.labels = dict()
    def colect(self, label, point, value):
        if not self.labels.has_key(label):
            self.labels[label] = []
        while len(self.labels[label]) <= point:
            self.labels[label] += [[]]
        self.labels[label][point] += [value]
    def __repr__(self):
        ret = "iter"
        labels = self.labels.keys()
        labels.sort()
        for label in labels:
            ret += ",max-" + label + ",min-" + label + ",avg-" + label
        for iter in range(1, len(self.labels[labels[0]])):
            ret += "\n" + str(iter)
            for label in labels:
                mx = max(self.labels[label][iter])
                mn = min(self.labels[label][iter])
                avg = sum(self.labels[label][iter])*1.0/len(self.labels[label][iter])
                ret += ",%f,%f,%f" % (mx,mn,avg)
                #ret += str(self.labels[label][iter]) + ","
        return ret

if __main__:
    steps = 2000
    popsize = 500
    age = 10
    loop = 20
    creator = lambda: dejong_f1_individual()
    #creator = lambda: dejong_f5_individual()
    if len(sys.argv) > 1 and sys.argv[1] == "2":
        creator = lambda: dejong_f2_individual()
    if len(sys.argv) > 1 and sys.argv[1] == "3":
        creator = lambda: dejong_f3_individual()
    if len(sys.argv) > 1 and sys.argv[1] == "4":
        creator = lambda: dejong_f4_individual()
    if len(sys.argv) > 1 and sys.argv[1] == "5":
        creator = lambda: dejong_f5_individual()
    stats4 = stats_colector()
    stats3 = stats_colector()
    stats2 = stats_colector()
    stats1 = stats_colector()
    stats0 = stats_colector()
    #stats0 = stats1 = stats2 = stats3 = stats4 = None
    for i in range(0, loop):
        ga = asyncga(creator, popsize, age, stats0)
        ga.run(steps, 0, 0)
        ga = strategy1(creator, popsize, age, stats1)
        ga.run(steps, 0, 0)
        ga = strategy2(creator, popsize, age, stats2)
        ga.run(steps, 0, 0)
        ga = strategy3(creator, popsize, age, stats3)
        ga.run(steps, 0, 0)
        ga = strategy4(creator, popsize, age, stats4)
        ga.run(steps, 0, 0)
    print stats0
    print stats1
    print stats2
    print stats3
    print stats4
    