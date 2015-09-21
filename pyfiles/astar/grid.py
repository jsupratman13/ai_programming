#grid test sample by redblobgames
#remember grid is rectangel box while graph is node + edges

import math

#square grid of 20x10 rectangele
all_nodes = []
for x in range(20):
	for y in range(10):
		all_nodes.append([x,y])
#print all_nodes

#edge will have four directions(dirs)
#node connected to other node by an edge is called neighbors
#if graph have diagonal movement you will have eight entries in dirs

def neighbors(node):
	dirs = [[1,0], [0,1], [-1,0], [0,-1]]
	result = []
	for dir in dirs:
		neighbor=[node[0] + dir[0], node[1] + dir[1]]
		if neighbor in all_nodes:
			result.append(neighbor)
	print result

#alternate wayt to makes sure coordinates are in range
#ex for 20x10 rectangular map

'''
def neighbors(node):
	dirs = [[1,0], [0,1], [-1,0], [0,-1]]
	result = []
	for dir in dirs:
		neighbor = [node[0] + dir[0], node[1] + dir[1]]
		if 0 <= neighbor[0] < 20 and 0 <= neighbor[1] < 10:
			result.append(neighbor)
'''  
