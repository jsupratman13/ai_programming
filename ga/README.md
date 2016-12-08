#Genetic Algorithm
Genetic Algorithm of (GA) is a search-based optimization technique based of the principles of Genetic and Natural selection or better known as 'survival of the fittest'. Often used to find optimal or near optimal solutions to problem that might take lifteime to solve. Thus it is useful in situation where it doesn't necessary have to find the 'best' solution but 'several good solutions' quickly.

##Advantages
* do not require derivative information (which is often occurs in real-world problems)
* fast and efficient
* good parallel capabilities
* optimize both continuous and discrete functions and also multi-objective problems
* provide lsit of good solutions not just one
* always gets an answer which gets better over time
* useful in situation when search space is large and therea are a large number of parameters

##Disadvantages
* not suited for problems which are simple and where derivative information is available
* computationally expensive for some problem
* stochastic, doesn't guarantee optimal solution
* may not converge to solution if not implmented properly

##Terminology
* population: all posible solution of a given problem
* chromosomes: one section of population, one specific solution
* gene: one section of chromosomes, one information of solution
* allele: actual info in gene
* genotype: population in computation space, ex 1010100
* phenotype: population in actual world. ex coordinate x,y,z = 1,0,1
* for simple problems, phenotype and genotype are the same
* decode: process of transforming solution from genotype to phenotype 101 -> x=1,y=0,z=1
* encode: process of transforming solution from phenotype to genotype x=1,y=1,z=0 -> 110
* fitness function: function for determining suitablity of solution
* genetic operators: alter genetic composition of the offspring (crossover, mutation, selection, etc.)

##Basic Structure
* initialize population (random or heuristic)
* select parents from population
* apply crossover and mutation to produce new offspring
* offspring replace population

###Pseudo Code
```
initialize population
find fitness of population
while (termination criteria is has not reached):
	parent selection
	crossover with probability pc
	mutation with probability pm
	decode and fitness calculation
	survivor selection
	find best
return best
```

##Genotype Representation
* mapping suitable representation is important for GA to produce good solution
* represenation may change depending on situation

###Binary Representation
* simplest and widely used
* may represent boolean or 0,1 where x-term tells whether item x is picked(1) or not(0)
* use gray coding

###Real Valued Representation
* represent gene using continuous rather than discrete variable
* use real value or floating point numbers
* limited to computer computation

###Integer Representation
* discrete value where solution cannnot be binary(yes,no) is represented as integer
* ex North South East West -> 0,1,2,3

###Permutation Representation
* in many problems, solution is represented by an order of elements.
* ex travelling salesman problem (cost of distance to travel and find minimum cost)

##Population
* diversity of population must be maintained
* size should not be very large. find the optimal size through trial and error
* usually defined as two dimensional arry of size population, size x, chromosome size
###Population Inititialization
* random initialization: completely random solution
* heuristic initialization: use known heuristc for the problem (should not used often as it will not give diversity)
###Population Model
* steady state (incremental GA): generate one or two offsprings at each iteration and replace them
* generational: generate n offspring (n=population size) and replace entire population at end of iteration

##Fitness Function
function that check to see how 'fit' or 'good' the canditate solution is with respect to the problem
* should be fast
* return quantitative measure (either high or low)

##Parent Selection
Crucial to the convergence rate of GA. Too similar is not good. Maintain good diversity, avoid premature convergence (entire population has extremely fit solution).
###Fitness Proportionate Selection
* most popular ways of parent selection, every individual can become a parent. 
* probability of becoming a parent depends on the fitness, fitter individual have higher chance of mating.
* in image, its like a circular wheel with divided into n(number of solutions) pies with each portion describing fitness
* this is similar to how in particle filters select which particles to consider.
* this doesnt work when fitness have negative value
####Roulette Wheel Selection
* fixed point is chosen on the wheel and the wheel is rotated. region of the wheel which comes in front of the fixed point is chosen
```
calculate S = sum of fitness
generate random number between 0 and S
starting from the top of the population keep adding the fitness to the partial sum P until P<S
individual which p exceed s is the chosen individual
```
####Stochastic Universal Sampling
* similar to roulette but we have multiple fixed point
* this setup is better as high individuals get chosen at least once

###Tournament Selection
* select K individuals from population at random and select the best out of these to become a parent.
* can work even if fitness value is negative

###Rank Selection
* can work even if fitness value is negative
* used when individuals have close fitness value
* may cause loss of selection pressure (picking fitter indivdials more likely)
###Random Selection
* randomly select from existing population
* no selection pressure so this is usually avoided

##Crossover
* reproduction and biological crossover between two or more parents to produe one or more offsprings.
* type below is generic and some design their own crossover operators depending on situation
* denote as pc
###One Point Crossover
* random crossover point is selected and the tails of its parents are swapped to get new offsprings
```
0123456 -> 0123 456 -> 0123222
4444222 -> 4444 222 -> 4444456
```
###Multi Point Crossover
* generalized one point cross over where alternating segments are sqapped to get new offsprings
```
0123456 -> 01 234 56 -> 0144222
4444222 -> 44 442 22 -> 4423422
```	
###Uniform Crossover
* treat each gene seperately, decided whether to switch or not
* deciding the swith can be biased or non-biased
```
0123456 -> 4144426
4444222 -> 0423252
```
###Whole Arighmetic Recombination
* commonly used for integer representation by taking the weight average of the two parents by using the forumula
```
child1 = ax + (1-a)y
child2 = ax + (1-a)y
```
###Davis Order Crossover (OX1)
* used for premutation based crossover with intention of transmitting information about relative ordering to the offsprings
* create two random crossover point in the parent and copy the segment between them from the first parent to the first offspring
* starting from second crossover point in the second parent, copy the remaining unsued numbers from the second parent to the first child wrapping around the list
* repeat for the second child with the parents role reverse
###Others
* Partially Mapped Crossover (PMX)
* Order Based Crossover (OX2)
* Shuffle Crossover
* Ring Crossover etc.

##Mutation
* random tweak in the chromosome to get new solution
* used to maintain and introduce diversity in the genetic population is usually aplied with a low probability (if two high, GA becomes random search)
* denote pm
###Bit Flip Mutation
* select one or more random bits and flip them
* used in binary encoded GA
```
00011010 -> 01011010
```
###Random Resetting
* integer representation version for bit flip mutation
* one or more random interger is swapped to different values

###Swap Mutation
* select two positions at random and swap them
* commonly used in premutation based encoding
```
123456 -> 1 2 345 6 -> 163452
```
###Scramble Mutation
* popular in premutation representation
* subset genes is chosen and their values are scramble or shuffle randomly
```
123456 -> 12 345 6 -> 124536
```
###Inversion Mutation
* similar to scramble mutation except instead of shuffling it is inversed
```
123456 -> 12 345 6 -> 125436
```

##Survivor Selection
* select which chromosome will live and replace eliminated chromosome with new random chromosome


