import pygame
import sys
from random import randint


class Grid(object):
	def __init__(self):
		self.BLACK = (0,0,0)
		self.WHITE = (255,255,255)
		self.GREEN = (0,255,0)
		self.RED = (255,0,0)
		self.BLUE = (0,255,255)

		self.MARGIN = 5
		self.WIDTH = 73
		self.HEIGHT = 73
		self.WINDOW_SIZE = []
		self.grid_map = []

	def coordinateX(self, column):
		return (self.MARGIN+self.WIDTH)*column+self.MARGIN

	def coordinateY(self,row):
		return (self.MARGIN+self.HEIGHT)*row+self.MARGIN

	def get_color(self,x,y):
		for row in range(len(grid_map)):
			for column in range(len(grid_map[0])):
				cell = pygame.Rect([self.coordinateX(column),self.coordinateY(row), self.WIDTH, self.HEIGHT])
				if cell.collidepoint(x,y):
					return grid_map[row][column]

	def draw_grid(self):
		for row in range(len(grid_map)):
			for column in range(len(grid_map[0])):
				color = grid_map[row][column]
				pygame.draw.rect(screen,color, pygame.Rect([self.coordinateX(column),self.coordinateY(row),self.WIDTH,self.HEIGHT]))

	def use_grid1(self):
		RED = self.RED
		GREEN = self.GREEN
		
		grid_map = [[RED,GREEN,GREEN,RED,RED],
					[RED,RED,GREEN,RED,RED],
					[RED,RED,GREEN,GREEN,GREEN],
					[RED,RED,RED,RED,RED]]
		self.grid_map = grid_map
		return grid_map

	def use_grid2(self):
		WHITE = self.WHITE
		RED = self.RED
		grid_map = [[RED,WHITE,RED,WHITE],
					[WHITE,RED,WHITE,RED],
					[RED,WHITE,RED,WHITE],
					[WHITE,RED,WHITE,RED]]
		self.grid_map = grid_map
		return grid_map

	def use_grid3(self):
		W = self.WHITE
		R = self.RED
		B = self.BLUE
		G = self.GREEN
		grid_map = [[W,R,B,G,G],
					[G,B,R,R,R],
					[W,W,B,G,R],
					[B,G,R,W,W],
					[B,G,R,B,B]]
		self.grid_map = grid_map
		return grid_map
	
	def fit_window_to_grid(self):
		WIDTH = self.WIDTH
		HEIGHT = self.HEIGHT
		MARGIN = self.MARGIN
		self.WINDOW_SIZE = [len(grid_map[0])*(WIDTH+MARGIN)+MARGIN, len(grid_map)*(HEIGHT+MARGIN)+MARGIN]
		return self.WINDOW_SIZE

class MonteCarlo(object):
	def __init__(self, world):
		self.p_move = 1
		self.p_sensor = 0.7
		self.grid_map = world
		self.grid_prob = self.uniform_distribution(self.grid_map)
	
	def uniform_distribution(self,world):
		grid_prob = []
		total_cell = len(world)*len(world[0])
		for i in range(len(world)):
			row = []
			for j in range(len(world[0])):
				row.append(1./total_cell)
			grid_prob.append(row)
		return grid_prob
	
	def bayes_rule(self,measurement):
		q = []
		total_cell = 0

		#accuracy
		pHit = self.p_sensor
		pMiss = 1-pHit
	
		#update measured probability * prior
		for i in range(len(self.grid_prob)):
			row = []
			for j in range(len(self.grid_prob[0])):
				hit = (measurement == self.grid_map[i][j])
				row.append(self.grid_prob[i][j] * (hit*pHit + (1-hit)*pMiss))
			total_cell += sum(row)
			q.append(row)
		
		#normalize
		for i in range(len(self.grid_prob)):
			for j in range(len(self.grid_prob[0])):
				q[i][j] /= total_cell

		self.grid_prob = q

	def total_probability(self, motion):
		q = []
		pExact = self.p_move
		
		#update movement
		for i in range(len(self.grid_prob)):
			row = []
			for j in range(len(self.grid_prob[0])):
				row.append(pExact*self.grid_prob[(i-motion[0])%len(self.grid_prob)][(j-motion[1])%len(self.grid_prob[0])])
			q.append(row)

		self.grid_prob = q
	
	def localize(self, measurement,motion):
		self.total_probability(motion)
		self.bayes_rule(measurement)

	def set_noise(self, sensor_accuracy,motion_accuracy):
		self.p_sensor = sensor_accuracy
		self.p_move = motion_accuracy

	def show(self):
		for row in range(len(self.grid_prob)):
			print '[',
			for column in range(len(self.grid_prob[0])):
				print '%2f' % self.grid_prob[row][column],
			print ']'

	
if __name__ == '__main__':
	grid = Grid()
	
	BLACK = grid.BLACK
	WIDTH = grid.WIDTH
	HEIGHT = grid.HEIGHT
	MARGIN = grid.MARGIN
	
	grid_map = grid.use_grid3()

	pygame.init()
	
	WINDOW_SIZE = grid.fit_window_to_grid()
	screen = pygame.display.set_mode(WINDOW_SIZE)
	pygame.display.set_caption("wandering renge")
	clock = pygame.time.Clock()

	im = pygame.image.load('renge.png').convert_alpha()
	rect = im.get_rect()
	init_x = randint(0,len(grid_map[0])-1)
	init_y = randint(0,len(grid_map)-1)
	rect.center = (pygame.Rect(grid.coordinateX(init_x),grid.coordinateY(init_y),WIDTH,HEIGHT)).center

	update_flag = False
	motion = [0,0]
	renge = MonteCarlo(grid_map)
	renge.show()
	while True:
		pygame.display.update()
		clock.tick(60)
		screen.fill(BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				update_flag = True
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == pygame.K_LEFT: rect.move_ip(-WIDTH-MARGIN,0); motion = [0,-1]
				elif event.key == pygame.K_RIGHT: rect.move_ip(WIDTH+MARGIN,0); motion = [0, 1]
				elif event.key == pygame.K_UP: rect.move_ip(0,-HEIGHT-MARGIN); motion = [-1, 0]
				elif event.key == pygame.K_DOWN: rect.move_ip(0,HEIGHT+MARGIN); motion = [1, 0]
				else: motion = [0,0]
		grid.draw_grid()

		if rect.centerx > WINDOW_SIZE[0]: rect.centerx = (grid.coordinateX(0)+WIDTH/2)
		if rect.centerx < 0: rect.centerx = (grid.coordinateX(len(grid_map[0])-1)+WIDTH/2)
		if rect.centery > WINDOW_SIZE[1]: rect.centery = (grid.coordinateY(0)+HEIGHT/2)
		if rect.centery < 0: rect.centery = (grid.coordinateY(len(grid_map)-1)+HEIGHT/2)
		screen.blit(im,rect)

		if update_flag:
			color = grid.get_color(rect.centerx, rect.centery)
			renge.localize(color,motion)
			print '------------------------------------------------'
			renge.show()
		update_flag = False



