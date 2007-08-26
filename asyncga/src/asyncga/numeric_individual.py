"""Numeric individual
"""
from asyncga.individual import individual
from random import uniform
from random import randint

class numeric_individual(individual):
    """that's the tradicional numeric individual
    each chromossome is a real number and stuff.
    """
    def __init__(self, size=0, min = 0, max = 100):
        self.chromossome = [uniform(min, max) for i in range(0, size)]
        self.size = size
        self.min = min
        self.max = max

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
        self.chromossome[mutationpoint] = uniform(self.min, self.max)
        #print "mutated pos", mutationpoint, "from", old, "to", self.chromossome[mutationpoint]
        return self
    def evaluate(self, model=None):
        """still not implemented here
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
    def evaluate(self, model=None):
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
    def evaluate(self, model=None):
        """evaluates dejong's f'
        """
        x1 = self.chromossome[0]
        x2 = self.chromossome[1]
        return 100*((x1**2 - x2)**2) + (1 - x1)**2
    def __repr__(self):
        return "F2 Individual: " + repr(self.chromossome)
    