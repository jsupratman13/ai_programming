Notes for Astar search

##Grid and Graph

##Breadth First Search
###The key idea for all of these algorithms is to keep track of an expanding ring called frontier.
###implementation
###1.pick and remove LOCATION from FRONTIER
###2.mark the location as VISITED to not repeat the same process
###3.expand the ring by looking for NEIGBORS(see grid.py for more info). any neighbors not seen yet is added to frontier.

##Dijkstra's Algorithm
###similar to breadth first search, it utilize cost of movement in path finding
###starts from the start and explores all possibility until goal

##Heuristic Search
###Heuristic is a technique to find problem quickly at the cost of accuracy etc. Basically a rough estimation
###fast but doesnt guarantee the best path
###starts from goal and head toward the start

##Astar
###dijkstra finds the best shortest path but waste time exploring all other option while greedy best explores the promising direction but not the best shortest path. 
###astar utilize both distance from start and estimation from goal
###similar to dijkstra, it explore the same set of location but the heuristic function visit the LOCATION in diffrent order

##Which path?
###Find path for all: Breadth if movement cost is same, Dijkstra if movment cost vary
###find path to one: use Astar or greedy (if greedy use astar if inadmissible heurisitc)
###inadmissible cost is to never overestimate the cost to the goal ex. total cost is lower than the lowest cost to goal


