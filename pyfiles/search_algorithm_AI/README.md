#Search Based Algorithm
Search Based Algorithm is usually used in finding the optimal solution to problems. It is typically used in path planning.

##Category
###Single Solution
Finds an optimal solution
####Without Cost
Search for an optimal solution without considering the characteristic of each node
* depth first search
* breadth first search
####With Cost
Search for an optimal solution while considering the characteristic of each node
* dijkstra algorithm
* greedy best search
* a star algorithm

###Multiple Solution
Finds multiple best solutions
* dynamic programming (only in interaction)
* genetic algorithm

#Heuristic
##Euclidean Distance
* distance between two points

|sqrt(2)|1|sqrt(2)|
---|---|---
|1|x|1|
|sqrt(2)|1|sqrt(2)|
```
cost = sqrt((x1-x2)**2 + (y1-y2)**2)
```

##Chebyshev Distance
* all adjacent cell is 1

1|1|1
---|---|---
1|x|1
1|1|1
```
cost = max(abs(x1-x2),abs(y1-y2))
```

##Manhattan Distance
* up,down,left,right is 1, diagonal is 2

2|1|2
---|---|---
1|x|1
2|1|2
```
cost = abs(x1-x2) + abs(y1-y2)
```


