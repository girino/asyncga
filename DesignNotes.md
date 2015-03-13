#General notes to guide the design process

# Notes #
## iterations ##
I am thinking of implementing the operations (mating, mutating, dying, etc) as a set of operators that apply iteratively over the population as a whole.

dying probability should be dependent on population size. Maybe use some quadratic formula to calculate the limit age, then a gaussian probability to decide if individuals must die!

# Update Aug 28 #
I finished implementing a simple stuff, now the GA is able to:
  * do all traditional GA does (roulete select, mate, mutate)
  * aging
  * die :) Dying is implemented in teh following ways:
    * age
    * age adjusted by fitness (fittest die older).

Just to note, when reproducing, only part of the population is created (something like n/maxage individuals) so they can live with older generations without overpopulation.

## Update August 31 ##
Done:
  * Stochastic number of new offspring (need to figure out some formula)
  * Stochastic dying (not only adjust age acording to fitness, but introducing some randomness too).

## Needs to do ##
Remodel the whole thing so as to have "independent" individuals. What I plan to do:
  * Each individual calculates it's own probability of breading/mating and of dying.
  * Then I iterate through the whole colection of individuals breading and killing acording to the probabilities.
  * Population sizes should be taken into acount for theses probability calculations (small pop, p(breeding) increases, p(death) decreases - Big pop, the oposite occurs).
This is a whole new thing, much different from the original GA concept, and from what I implemented up to now.