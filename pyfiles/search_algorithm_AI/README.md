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


