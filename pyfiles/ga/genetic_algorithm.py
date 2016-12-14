from random import randint, random
from operator import add

def create_chromosome(length, min_val,max_val):
    #length: number of gene in chromosome
    #max_val,min_val: randomize allele within these value
    return [randint(min_val,max_val) for x in xrange(length)]

def create_population(count, length, min_val, max_val):
    #count: number of chromosome in population
    #length: number of gene in chromosome
    #max_val,min_val: randomize allele within these value
    return [create_chromosome(length, min_val, max_val) for x in xrange(count)]

def fitness_function(chromosome, target):
    total = reduce(add,chromosome,0)
    #total = reduce(lambda x,y: x+y, chromosome,0)
    return abs(target-total)

def grade(population,target):
    #find average fitness of population
    avg = reduce(add,(fitness_function(chromosome,target) for chromosome in population))
    return avg/(len(population)*1.0)

def evolve(population, target, retain=0.2, random_select=0.5, mutate=0.01):
    graded = [(fitness_function(chromosome, target), chromosome) for chromosome in population]
    graded = [ x[1] for x in sorted(graded)]
    retain_length = int(len(graded)*retain)
    parents = graded[:retain_length]
    #randomly add indviduals to promote genetic diversity
    for individual in graded[retain_length:]:
        if random_select > random():
            parents.append(individual)
    #mutate some individual: RANDOM RESETTING
    for individual in parents:
        if mutate > random():
            position_to_mutate = randint(0,len(individual)-1)
            individual[position_to_mutate] = randint(min(individual), max(individual))
    #crossover: MULTIPOINT CROSSOVER
    parents_length = len(parents)
    desired_length = len(population) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)
        if male != female:  
            male = parents[male]
            female = parents[female]
            half = len(male)/2
            child = male[:half] + female[half:]
            children.append(child)
    parents.extend(children)
    return parents

if __name__ == '__main__':
#Example problem: Create a list of N numbers where sum equals to the target value
#ex: N=5, target = 200, list=[40,40,40,40,40]or[50,50,50,25,25]or[200,0,0,0,0]

    target = 371
    number_of_population = 100
    length_of_chromosome = 5
    min_length = 0
    max_length = 100
    p = create_population(number_of_population, length_of_chromosome, min_length, max_length)
    fitness_history = [grade(p,target),]
    for i in xrange(100):
        p = evolve(p,target)
        fitness_history.append(grade(p,target))
    print 'fitness history: '
    print fitness_history
    print 'best population result '
    print p[0]
    print 'target: '+str(target)+ ' population: ' + str(sum(p[0]))

