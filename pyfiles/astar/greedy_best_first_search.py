#greedy best first search with heuristic function + breadth fist search
import grid
import math
from Queue import PriorityQueue()


def heurisitc(a, b):
	#in terms of grid not graph
	return math.abs(a.x - b.x) + (a.y -b.y)

frontier = PriorityQueue()
frontier.put(start,0)
came_from = {}
came_from[start] = None
while not frontier.empty():
	current = frontier.get()
	if current == goal:
		break
	for next in graph.neighbors(current):
		if next not in came_from:
			priority = heuristic(goal, next)
			frontier.put(next, priority)
			came_from[next] = current
