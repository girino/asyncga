"""asyncga.individual
"""

class individual:
    """interface of an actual individual
    """
    def mate(self, other):
        """mates this individual with another (of same type)
        """
    def clone(self):
        """Makes a new individual exactly like myself
        """
    def mutate(self):
        """Gosh, i got some gama rays into altering my DNA.
        """
    def get_age(self):
        """this is generic to the whole framework, so
        I really implement this here!
        """
        return self.age
    def make_older(self):
        self.age = self.age + 1
    def evaluate(self, model=None):
        """this is the whole point of GA: a fitness function.
        """
    
    