#Similar to breadth first search but also include costs
import grid
from Queue import PriorityQueue

frontier = PriorityQueue()
frontier.put(start, 0)
came_from = {}
cost_so_far = {}
came_from[start] = None
cost_so_far[start] = 0

while not frontier.empty():
	current = frontier.get()
	if current == goal:
		break
	for next in graph.neighbors(current):
		new_cost = cost_so_far[current] + grid.cost(current, next) #TODO: implement on grid.py cost
		if next not in cost_so_far or new_cost < cost_so_far[next]:
			cost_so_far[next] = new_cost
			priority = new_cost
			frontier.put(next,priority)
			came_from[next] = current
	
