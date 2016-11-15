import pygame
import sys,copy,math
from random import randint

class Grid(object):
	def __init__(self):
		self.BLACK = (0,0,0)
		self.WHITE = (255,255,255)
		self.GREEN = (0,255,0)
		self.RED = (255,0,0)
		self.BLUE = (0,255,255)
		self.YELLOW = (255,255,0)

		self.MARGIN = 5
		self.WIDTH = 73
		self.HEIGHT = 73
		self.WINDOW_SIZE = []
		self.grid_map = []

	def up(self,column,row):
		x = self.coordinateX(column)
		y = self.coordinateY(row)
		pygame.draw.line(screen,self.RED,[x,y+self.HEIGHT],[x+(self.WIDTH/2),y], 2)
		pygame.draw.line(screen,self.RED,[x+(self.WIDTH/2),y],[x+self.WIDTH,y+self.HEIGHT], 2)
	
	def down(self, column, row):
		x = self.coordinateX(column)
		y = self.coordinateY(row)
		pygame.draw.line(screen,self.RED,[x,y],[x+(self.WIDTH/2),y+self.HEIGHT], 2)
		pygame.draw.line(screen,self.RED,[x+(self.WIDTH/2),y+self.HEIGHT],[x+self.WIDTH,y], 2)

	def left(self, column, row):
		x = self.coordinateX(column)
		y = self.coordinateY(row)
		pygame.draw.line(screen,self.RED,[x,y],[x+self.WIDTH,y+(self.HEIGHT/2)], 2)
		pygame.draw.line(screen,self.RED,[x+self.WIDTH,y+(self.HEIGHT/2)],[x,y+self.HEIGHT], 2)

	def right(self, column, row):
		x = self.coordinateX(column)
		y = self.coordinateY(row)
		pygame.draw.line(screen,self.RED,[x+self.WIDTH,y],[x,y+(self.HEIGHT/2)], 2)
		pygame.draw.line(screen,self.RED,[x,y+(self.HEIGHT/2)],[x+self.WIDTH,y+self.HEIGHT], 2)

	def coordinateX(self, column):
		return (self.MARGIN+self.WIDTH)*column+self.MARGIN

	def coordinateY(self,row):
		return (self.MARGIN+self.HEIGHT)*row+self.MARGIN

	def draw_grid(self,grid):
		for row in range(len(grid)):
			for column in range(len(grid[0])):
				color = grid[row][column]
				pygame.draw.rect(screen,color, pygame.Rect([self.coordinateX(column),self.coordinateY(row),self.WIDTH,self.HEIGHT]))

	def draw_path(self,path):
		for row in range(len(path)):
			for column in range(len(path[0])):
				direction = path[row][column]
				if direction == '^':
					self.up(column,row)
				elif direction == 'V':
					self.down(column,row)
				elif direction == '<':
					self.right(column,row)
				elif direction == '>':
					self.left(column,row)

	def use_grid(self):
		W = self.WHITE
		Y = self.YELLOW
		B = self.BLACK
		
		grid_map = [[W,B,W,W,W,W],
					[W,B,W,W,W,W], 
					[W,B,W,W,W,W],
					[W,B,W,W,W,W],
					[W,W,W,W,W,W]]
		self.grid_map = grid_map
		return grid_map

	def use_grid2(self):
		W = self.WHITE
		grid_map = [[W for col in range(10)] for row in range(10)]
		self.grid_map = grid_map
		return grid_map

	def fit_window_to_grid(self):
		WIDTH = self.WIDTH
		HEIGHT = self.HEIGHT
		MARGIN = self.MARGIN
		self.WINDOW_SIZE = [len(grid_map[0])*(WIDTH+MARGIN)+MARGIN, len(grid_map)*(HEIGHT+MARGIN)+MARGIN]
		return self.WINDOW_SIZE

	def grid_animation(self, grid):
		self.draw_grid(grid)
		screen.blit(im,rect)
		screen.blit(im2,rect2)
		pygame.display.update()
		pygame.time.delay(100)

class Search(object):
	def __init__(self, world):
		self.world = world;
		self.grid = copy.deepcopy(world.grid_map)
		self.BLACK = world.BLACK
		self.BLUE = world.BLUE
		self.WHITE = world.WHITE
		
		#movement
		self.motions = [[-1,0],#up
						[0,-1],#left
						[1, 0],#down
						[0, 1]]#right
		self.motion_name = ['^','<','V','>']

	def reset(self, grid,start=None, goal=None):
		#search area
		self.grid = copy.deepcopy(grid)
		self.expand = copy.deepcopy(self.grid)
		self.frontier = [[0 for row in range(len(self.grid[0]))] for col in range(len(self.grid))]

		#initial
		self.g = 0
		if start:
			self.x = (rect.centery - self.world.MARGIN)/(self.world.MARGIN+self.world.HEIGHT)
			self.y = (rect.centerx - self.world.MARGIN)/(self.world.MARGIN+self.world.WIDTH)

		#goal
		if goal:
			goal_x = (goal.centery - self.world.MARGIN)/(self.world.MARGIN + self.world.HEIGHT)
			goal_y = (goal.centerx - self.world.MARGIN)/(self.world.MARGIN + self.world.WIDTH)
		self.goal = [goal_x,goal_y]
	
		#close list to prevent node from being searched again open:0, close:1
		self.closed = [[0 for row in range(len(self.grid[0]))] for col in range(len(self.grid))]
		self.closed[self.x][self.y] = 1

		#show decided path
		self.action = [[-1 for row in range(len(self.grid[0]))] for col in range(len(self.grid))]
		self.path = [[' ' for row in range(len(self.grid[0]))] for col in range(len(self.grid))]

		#show value
		self.value = [[999 for row in range(len(self.grid[0]))]for col in range(len(self.grid))]

	def set_heuristic(self):
		#use euclidean distance
		self.heuristic = [[1000 for row in range(len(self.grid[0]))] for col in range(len(self.grid))]
		for col in range(len(self.grid[0])):
			for row in range(len(self.grid)):
				self.heuristic[row][col] = abs(self.goal[0]-row) + abs(self.goal[1]-col)

	def get_path(self, action=None):
		if action:
			self.action = action
		x = self.goal[0]
		y = self.goal[1]
		self.path[x][y] = '*'
		while x != self.x or y != self.y:
			x2 = x - self.motions[self.action[x][y]][0]
			y2 = y - self.motions[self.action[x][y]][1]
			self.path[x2][y2] = self.motion_name[self.action[x][y]]
			x = x2
			y = y2
		return self.path

	def get_policy(self):
		update = True
		while update:
			update = False
			for x in range(len(self.grid)):
				for y in range(len(self.grid[0])):
					if x == self.goal[0] and y == self.goal[1]:
						if self.value[x][y] != 0:
							self.value[x][y] = 0
							self.path[x][y] = '*'
							update = True
					elif self.grid[x][y] == self.WHITE:
						for i in range(len(self.motions)):
							x2 = x + self.motions[i][0]
							y2 = y + self.motions[i][1]
							if x2 >= 0 and x2 < len(self.grid) and y2 >= 0 and y2 < len(self.grid[0]):
								if self.grid[x][y] != self.BLACK:
									value = self.value[x2][y2] + 1
									if value < self.value[x][y]:
										self.value[x][y] = value
										self.path[x][y] = self.motion_name[i]
										update = True
		return self.path

	def breadthfirst(self):
		x = self.x
		y = self.y
		open_list = [[x,y]]
		while open_list:
			node = open_list.pop(0)
			x = node[0]
			y = node[1]

			if x == self.goal[0] and y == self.goal[1]:
				return self.expand
			else:
				self.expand[x][y] = self.BLUE
				self.world.grid_animation(self.expand)
				for i in range(len(self.motions)):
					x2 = x + self.motions[i][0]
					y2 = y + self.motions[i][1]
					if x2 >= 0 and x2 < len(self.expand) and y2 >= 0 and y2 < len(self.expand[0]):
						if self.closed[x2][y2] == 0 and self.expand[x2][y2] != self.BLACK:
							open_list.append([x2,y2])
							self.closed[x2][y2] = 1
							self.action[x2][y2] = i
		print 'no plan found'
		return None

	def depthfirst(self):
		x = self.x
		y = self.y
		open_list = [[x,y]]
		while open_list:
			node = open_list.pop()
			x = node[0]
			y = node[1]

			if x == self.goal[0] and y == self.goal[1]:
				return self.expand
			else:
				self.expand[x][y] = self.BLUE
				self.world.grid_animation(self.expand)
				for i in range(len(self.motions)):
					x2 = x + self.motions[i][0]
					y2 = y + self.motions[i][1]
					if x2 >= 0 and x2 < len(self.expand) and y2 >= 0 and y2 < len(self.expand[0]):
						if self.closed[x2][y2] == 0 and self.expand[x2][y2] != self.BLACK:
							open_list.append([x2,y2])
							self.closed[x2][y2] = 1
							self.action[x2][y2] = i
		print 'no plan found'
		return None

	def dijkstra(self):
		g = self.g
		x = self.x
		y = self.y
		open_list = [[g,x,y]]
#		index = 0
		while open_list:
			open_list.sort()
			node = open_list.pop(0)
			x = node[1]
			y = node[2]
			g = node[0]

#			index += 1
#			self.frontier[x][y] = index
			if x == self.goal[0] and y == self.goal[1]:
#				print node
#				for c in self.frontier:
#					print c
				return self.expand
			else:
				self.expand[x][y] = self.BLUE
				self.world.grid_animation(self.expand)
				for i in range(len(self.motions)):
					x2 = x + self.motions[i][0]
					y2 = y + self.motions[i][1]
					if x2 >= 0 and x2 < len(self.expand) and y2 >= 0 and y2 < len(self.expand[0]):
						if self.closed[x2][y2] == 0 and self.expand[x2][y2] != self.BLACK:
							g += 1
							open_list.append([g,x2,y2])
							self.closed[x2][y2] = 1
							self.action[x2][y2] = i
		print 'no plan found'
		return None

	def greedy(self):
		x = self.x
		y = self.y
		h = self.heuristic[x][y]
		open_list = [[h,x,y]]
		while open_list:
			open_list.sort()
			node = open_list.pop(0)
			x = node[1]
			y = node[2]
			h = node[0]

			if x == self.goal[0] and y == self.goal[1]:
#				print node
				return self.expand
			else:
				self.expand[x][y] = self.BLUE
				self.world.grid_animation(self.expand)
				for i in range(len(self.motions)):
					x2 = x + self.motions[i][0]
					y2 = y + self.motions[i][1]
					if x2 >= 0 and x2 < len(self.expand) and y2 >= 0 and y2 < len(self.expand[0]):
						if self.closed[x2][y2] == 0 and self.expand[x2][y2] != self.BLACK:
							h = self.heuristic[x2][y2]
							open_list.append([h,x2,y2])
							self.closed[x2][y2] = 1
							self.action[x2][y2] = i
		print 'no plan found'
		return None

	def astar(self):
		g = self.g
		x = self.x
		y = self.y
		f = g + self.heuristic[x][y]
		open_list = [[f,x,y,g]]
		while open_list:
			open_list.sort()
			node = open_list.pop(0)
			f = node[0]
			x = node[1]
			y = node[2]
			g = node[3]
			
			if x == self.goal[0] and y == self.goal[1]:
#				print node
				return self.expand
			else:
				self.expand[x][y] = self.BLUE
				self.world.grid_animation(self.expand)
				for i in range(len(self.motions)):
					x2 = x + self.motions[i][0]
					y2 = y + self.motions[i][1]
					if x2 >= 0 and x2 < len(self.expand) and y2 >= 0 and y2 < len(self.expand[0]):
						if self.closed[x2][y2] == 0 and self.expand[x2][y2] != self.BLACK:
							f = g + self.heuristic[x2][y2]
							g += 1
							open_list.append([f,x2,y2,g])
							self.closed[x2][y2] = 1
							self.action[x2][y2] = i
		print 'no plan found'
		return None
	
if __name__ == '__main__':
	grid = Grid()

	YELLOW = grid.YELLOW
	BLACK = grid.BLACK
	WHITE = grid.WHITE
	WIDTH = grid.WIDTH
	HEIGHT = grid.HEIGHT
	MARGIN = grid.MARGIN
	
	grid_map = grid.use_grid2()

	pygame.init()
	
	WINDOW_SIZE = grid.fit_window_to_grid()
	screen = pygame.display.set_mode(WINDOW_SIZE)
	pygame.display.set_caption("wandering renge")
	clock = pygame.time.Clock()

	im = pygame.image.load('renge.png').convert_alpha()
	rect = im.get_rect()
	init_x = 0
	init_y = 0
	rect.center = (pygame.Rect(grid.coordinateX(init_x),grid.coordinateY(init_y),WIDTH,HEIGHT)).center

	im2 = pygame.image.load('star.png').convert_alpha()
	im2 = pygame.transform.scale(im2, (WIDTH, HEIGHT))
	rect2 = im2.get_rect()
	init_x = len(grid_map[0])-1
	init_y = len(grid_map)-1
	rect2.center = (pygame.Rect(grid.coordinateX(init_x), grid.coordinateY(init_y), WIDTH, HEIGHT)).center

	expand = None
	search = Search(grid)
	obs_flag = None
	pos_flag = None
	policy = False
	while True:
		pygame.display.update()
		clock.tick(60)
		screen.fill(BLACK)

		#change grid
		mouse_pressed = pygame.mouse.get_pressed()
		if mouse_pressed[0]:
			expand = None
			policy = False
			x,y = pygame.mouse.get_pos()
			if not x <0 and not y <0 and not x >= WINDOW_SIZE[0]-MARGIN and not y >= WINDOW_SIZE[1]-MARGIN:
				column = x // (WIDTH+MARGIN)
				row = y // (HEIGHT+MARGIN)
				if rect.collidepoint(x,y):
					pos_flag = rect
					rect.center = (x,y)
					obs_flag = WHITE
				elif rect2.collidepoint(x,y):	
					pos_flag = rect2
					rect2.center = (x,y)
					obs_flag = WHITE
				else:
					if grid.grid_map[row][column] == BLACK and not obs_flag:
						obs_flag = WHITE
					elif grid.grid_map[row][column] == WHITE and not obs_flag:
						obs_flag = BLACK
				if obs_flag:
					grid.grid_map[row][column] = obs_flag
		else:
			if pos_flag:
				pos_flag.center = (pygame.Rect(grid.coordinateX(column), grid.coordinateY(row),WIDTH,HEIGHT)).center
			obs_flag = None
			pos_flag = None

		#key command
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			#excute command
			if event.type == pygame.KEYDOWN:
				search.reset(grid.grid_map,start=rect,goal=rect2)
				expand = None
				policy = False
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
				#press b for breadth first
				if event.key == pygame.K_b:
					print 'breadth first search'
					expand = search.breadthfirst()
				#press d for depth first
				if event.key == pygame.K_d:
					print 'depth first search'
					expand = search.depthfirst()
				#press u for dijkstra (uniform cost)
				if event.key == pygame.K_u:
					print 'dijkstra algorithm'
					expand = search.dijkstra()
				#press a for astar
				if event.key == pygame.K_a:
					print 'a* algorithm'
					search.set_heuristic()
					expand = search.astar()
				#press g for greedy
				if event.key == pygame.K_g:
					print 'greedy algorithm'
					search.set_heuristic()
					expand = search.greedy()
				#press p to show policy
				if event.key == pygame.K_p:
					print 'showing policy'
					path =  search.get_policy()
					policy = True
				if expand:
					path = search.get_path()

		if expand:
			grid.draw_grid(expand)
			grid.draw_path(path)
		else:
			grid.draw_grid(grid.grid_map)
			if policy: grid.draw_path(path)

		screen.blit(im,rect)
		screen.blit(im2,rect2)



