import pygame
from pygame.locals import *
import sys, math, time,copy
from players_fsm import Player, Enemy
from powerup import Powerup

class Game:
	def __init__(self):
		(w,h) = (800,800)
		pygame.init()
		pygame.display.set_mode((w,h), 0, 32)
		self.screen = pygame.display.get_surface()
		
		self.player = Player(self.screen.get_rect())
		self.player_list = [self.player]		

		self.enemy = Enemy(400,100)
		self.enemy_list = [self.enemy]

		self.respawn = False
		self.respawn_time = time.time()

		self.power_up = Powerup(self.screen)

	def run(self):
		pygame.display.update()
		pygame.time.wait(30)
		self.screen.fill((0,20,0,0))
		pressed_key = pygame.key.get_pressed()
		
		#player
		for p in self.player_list:
			p.key_handler(pressed_key)
			p.update(self.screen)
			p.hit_target(self.enemy_list)
			if not p.is_alive:
				print 'player destroyed'
				self.player_list.remove(p)
		
		#enemy
		for e in self.enemy_list:
			e.update(self.screen, self.player_list)
			e.hit_target(self.player_list)
			if not e.is_alive:
				print 'enemy destroyed'
				self.enemy_list.remove(e)

		#respawn enemy
		if not self.respawn and (not self.enemy_list or not self.player_list):
			self.respawn_time = time.time()
			self.respawn = True

		if time.time() - self.respawn_time > 3 and self.respawn:
			self.respawn_time = time.time()
			self.respawn = False
			if not self.enemy_list:
				self.enemy_list.append(Enemy(400,100))
			if not self.player_list:
				self.player_list.append(Player(self.screen.get_rect()))

		#powerup
		self.power_up.update(self.player_list)

		#event
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
if __name__ == '__main__':
	game = Game()
	while True:
		game.run()
