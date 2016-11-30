#Breadth First Search

import grid
from Queue import Queue

#basic frontier expansion ring
frontier = Queue()
frontier.put(start) #start is all node
visited = {}
visited[start] = True 	# here we have to pick first visited place

while not frontier.empty():
	current = frontier.get()
	for next in grid.negihbors(current):
		if next not in visited:
			frontier.put(next)
			visited[next] = True

#modification to keep track of movment
frontier = Queue()
frontier.put(start)
came_from =[]
came_from[start] = True

while not frontier.empty():
	current = frontier.get()
	for next in grid.neighbors(current):
		if next not in came_from:
			frontier.put(next)
			came_from[next] = current

#reconstruction of path
current = goal 	#here we have goal
path = [current]
while current != start:
	current = came_from[current]
	path.append(current)
path.reverse()

#'eary exit' means to stop expanding the frontier as soon as the goal is found
frontier = Queue()
frontier.put(start)
came_from = {}
came_from[start] = None
while not frontier.empty():
	current = frontier.get()
	##early exit mode
	if current == goal:
		break
	for next in grid.neighbors(current):
		if next not in came_from:
			frontier.put(next)
			came_from[next] = current


