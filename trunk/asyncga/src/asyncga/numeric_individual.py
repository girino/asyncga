"""Numeric individual
"""
from asyncga.individual import individual
from random import uniform
from random import randint
from random import normalvariate
import random
import math

class numeric_individual(individual):
    """that's the tradicional numeric individual
    each chromossome is a real number and stuff.
    """
    def __init__(self, size=0, min = 0, max = 100):
        individual.__init__(self)
        self.chromossome = [uniform(min, max) for i in range(0, size)]
        self.size = size
        self.min = min
        self.max = max
        self.cache = None

    def make_instance(self):
        """MUST BE OVERIDDEN
        """
        return numeric_individual(0, self.min, self.max)

    def mate(self, other):
        crossingpoint = randint(0, self.size-1)
        ret = self.make_instance()
        ret.size = self.size
        ret.chromossome = self.chromossome[0:crossingpoint] + other.chromossome[crossingpoint:]
        return ret
    def clone(self):
        return self.mate(self)
    def mutate(self):
        mutationpoint = randint(0, self.size-1)
        #print mutationpoint
        old = self.chromossome[mutationpoint]
        stdev = (self.max - self.min)/4.0
        newvalue = normalvariate(old, stdev)
        # binds to limits
        newvalue = min([newvalue, self.max])
        newvalue = max([newvalue, self.min])
        self.chromossome[mutationpoint] = newvalue
        #print "mutated pos", mutationpoint, "from", old, "to", self.chromossome[mutationpoint]
        return self
    def evaluate(self, model=None):
        """
        This one calls the __evaluate__ method and caches it.
        """
        if not self.cache:
            self.cache = self.__evaluate__(model)
        return self.cache
    def __evaluate__(self, model=None):
        """
        This one is called and cached
        """
    def __repr__(self):
        return "Numeric Individual: " + repr(self.chromossome)
        
class dejong_f1_individual(numeric_individual):
    """implements individuals to solve dejong's f1
    """
    def __init__(self, empty=False):
        if empty:
            numeric_individual.__init__(self, 0, -5.12, 5.12)
        else:
            numeric_individual.__init__(self, 3, -5.12, 5.12)
    def make_instance(self):
        """MUST BE OVERIDDEN
        """
        return dejong_f1_individual(True)
    def __evaluate__(self, model=None):
        """evaluates dejong's f'
        """
        return sum([x*x for x in self.chromossome])
    def __repr__(self):
        return "F1 Individual: " + repr(self.chromossome)

class dejong_f2_individual(numeric_individual):
    """implements individuals to solve dejong's f1
    """
    def __init__(self, empty=False):
        if empty:
            numeric_individual.__init__(self, 0, -2.048, 2.048)
        else:
            numeric_individual.__init__(self, 2, -2.048, 2.048)
    def make_instance(self):
        """MUST BE OVERIDDEN
        """
        return dejong_f2_individual(True)
    def __evaluate__(self, model=None):
        """evaluates dejong's f'
        """
        x1 = self.chromossome[0]
        x2 = self.chromossome[1]
        return 100*((x1**2 - x2)**2) + (1 - x1)**2
    def __repr__(self):
        return "F2 Individual: " + repr(self.chromossome)

class dejong_f3_individual(numeric_individual):
    """implements individuals to solve dejong's f3
    """
    def __init__(self, empty=False):
        if empty:
            numeric_individual.__init__(self, 0, -5.12, 5.12)
        else:
            numeric_individual.__init__(self, 5, -5.12, 5.12)
    def make_instance(self):
        """MUST BE OVERIDDEN
        """
        return dejong_f3_individual(True)
    def __evaluate__(self, model=None):
        """evaluates dejong's f'
        """
        return sum([int(x) for x in self.chromossome])
    def __repr__(self):
        return "F3 Individual: " + repr(self.chromossome)
    
class dejong_f4_individual(numeric_individual):
    """implements individuals to solve dejong's f4
    """
    def __init__(self, empty=False):
        if empty:
            numeric_individual.__init__(self, 0, -1.28, 1.28)
        else:
            numeric_individual.__init__(self, 30, -1.28, 1.28)
        self.noise = random.gauss(0,1)
    def make_instance(self):
        """MUST BE OVERIDDEN
        """
        return dejong_f4_individual(True)
    def __evaluate__(self, model=None):
        """evaluates dejong's f'
        """
        ret = [math.pow(x, 4) for x in self.chromossome]
        ret = [i*ret[i] for i in range(0, len(ret))]
        return self.noise + sum(ret)
    def __repr__(self):
        return "F4 Individual: " + repr(self.chromossome)
    
class dejong_f5_individual(numeric_individual):
    """implements individuals to solve dejong's f5
    """
    def __init__(self, empty=False):
        if empty:
            numeric_individual.__init__(self, 0, -65.536, 65.536)
        else:
            numeric_individual.__init__(self, 2, -65.536, 65.536)
        self.noise = random.gauss(0,1)
    def make_instance(self):
        """MUST BE OVERIDDEN
        """
        return dejong_f5_individual(True)
    def __evaluate__(self, model=None):
        """evaluates dejong's f'
        """
        a = [[-32,-16,0,16,32] * 5, [-32] * 5 + [-16] * 5 + [0] * 5 + [16] * 5 + [32] * 5]
        x = self.chromossome
        ret = 0.002 + sum([1/(j + sum([math.pow(x[i] - a[i][j-1], 6) for i in range(0,2)])) for j in range(1, 26)])
        return 1.0/ret
    def __repr__(self):
        return "F5 Individual: " + repr(self.chromossome)