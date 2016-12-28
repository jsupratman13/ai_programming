#  0 1 2 3 4 5
# |-|-|-|-|-|-|
#0|s| |#| | | |
# |-|-|-|-|-|-|
#1| | |#| | | |
# |-|-|-|-|-|-|
#2| | | | |#| |
# |-|-|-|-|-|-|
#3| | |#|#|#| |
# |-|-|-|-|-|-|
#4| | | | |#|g|
# |-|-|-|-|-|-|

#Grid formt: 
#   0 = Navigable Space
#   1 = Occupied Space


grid = [[0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0]]

init = [0,0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

#manhattan distance
heuristic = [[100 for row in range(len(grid[0]))]for col in range(len(grid))]
for col in range(len(grid[0])):
    for row in range(len(grid)):
        heuristic[row][col] = abs(goal[0]-row) + abs(goal[1]-col)

delta = [[-1, 0], #go up
     [ 0,-1], #go left
     [ 1, 0], #go down
     [ 0, 1]] #go right

delta_name = ['^', '<', 'V', '>']


def search(grid, init, goal, cost,heuristic):
    #open list elements are of type [f,g,x,y]

    frontier = [[-1 for row in range(len(grid[0]))]for col in range(len(grid))]
    expansion = 0
    #get closed grid to prevent node from being checked again, 0 for open, 1 for closed
    closed_list = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed_list[init[0]][init[1]] = 1
    #path
    action = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]

    x = init[0]
    y = init[1]
    g = 0
    f = g + heuristic[x][y]

    open_list = [[f,g,x,y]]
    
    found = False #flag is set when search complete
    resign = False #flag when we cant find expand

    #print 'initial open list:'
    #for i in range(len(open)):
        #print '    ', open[i]
    #print '--------'

    while found is False and resign is False:
        #check if we still have elements on the open list
        if len(open_list) == 0:
            resign = True
            print 'no optimal path found'
        
        else:
            #remove node from list
            open_list.sort()
            open_list.reverse()
            node = open_list.pop()
            #print 'take list item'
            #print next
            x = node[2]
            y = node[3]
            g = node[1]
            f = node[0]
    
            #check what areas are searched
            frontier[x][y] = expansion
            expansion += 1
        
            #check if we are done
            if x == goal[0] and y == goal[1]:
                found = True
                print node
            else:
                # expand winning element and add to new open list
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]):
                        if closed_list[x2][y2] == 0 and grid [x2][y2] == 0:
                            g2 = g + cost
                            f = g2 + heuristic[x2][y2]
                            open_list.append([f,g2,x2,y2])
                            #print 'append list item"
                            #print [g2,x2,y2]
                            closed_list[x2][y2] = 1
                            action[x2][y2] = i


    path = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    x = goal[0]
    y = goal[1]
    path[x][y] = '*'
    if found:
        while x!= init[0] or y != init[1]:
            x2 = x - delta[action[x][y]][0]
            y2 = y - delta[action[x][y]][1]
            path[x2][y2] = delta_name[action[x][y]]
            x = x2
            y = y2
    return frontier, path

if __name__ == '__main__':
    frontier,path = search(grid,init,goal,cost,heuristic)
    for row in frontier:
        print row
    for row in path:
        print row
