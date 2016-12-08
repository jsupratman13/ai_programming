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


