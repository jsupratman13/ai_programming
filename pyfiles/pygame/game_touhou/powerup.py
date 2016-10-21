import pygame
from pygame.locals import *
from players import detect_collision

class Powerup:
	def __init__(self, screen):
		self.powerup = [Powerup.RapidPowerup(screen), \
				Powerup.SpeedPowerup(screen), \
				Powerup.LaserWeapon(screen)]

	def update(self, player_list):
		for p in self.powerup:
			for player in player_list:
				if detect_collision(p, player):
					p.contact = True
					p.upgrade(player)	
			
			p.update()

	class RapidPowerup:
		def __init__(self, screen):
			self.screen = screen
			self.contact = False
			self.x = 250
			self.y = 600
		
		def update(self):
			if not self.contact:
				pygame.draw.circle(self.screen, (255,0,0),(self.x, self.y),10)

		def upgrade(self,player):
			player.SHOT_SPEED = 0.5	

	class SpeedPowerup:
		def __init__(self,screen):
			self.screen = screen
			self.contact = False
			self.x = 650
			self.y = 600
	
		def update(self):
			if not self.contact:
				pygame.draw.circle(self.screen, (0,0,255),(self.x, self.y), 10)

		def upgrade(self, player):
			player.MOVE_SPEED = 5		

	class LaserWeapon:
		def __init__(self,screen):
			self.screen = screen
			self.contact = False
			self.x = 700
			self.y = 700

		def update(self):
			if not self.contact:
				pygame.draw.circle(self.screen, (0,255,0),(self.x, self.y),10)
		
		def upgrade(self, player):
			player.WEAPON = 1
