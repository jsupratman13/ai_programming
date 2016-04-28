import pygame
from pygame.locals import *
import time, math

class Bullet:
	def __init__(self, rect, angle, source):
		L = rect.top-rect.centery
		rx = L*math.sin(math.radians(angle))+rect.centerx
		ry = L*math.cos(math.radians(angle))+rect.centery
		self.angle = angle
		self.x = rx
		self.y = ry
		self.contact = False
		self.source = source
	
	def update(self,screen):
		self.y += -5*math.cos(math.radians(self.angle))
		self.x += -5*math.sin(math.radians(self.angle))
		if self.source == 'ENEMY':
			color = 0
		else:
			color = 255
		if not self.contact:
			pygame.draw.circle(screen, (255,color,255),(int(self.x), int(self.y)),5)
"""
class Bullet2:
	def __init__(self, rx, ry, source):
		self.x = rx
		self.y = ry
		self.source = source
		self.contact = False

	def update(self,screen):
		if self.source == 'ENEMY':
			self.y += 5
			color = 0
		else:
			color = 255
			self.y -= 5
		if not self.contact:
			pygame.draw.circle(screen, (255,color,255),(self.x, self.y),5)
"""
class Laser:
	def __init__(self, rx, ry, source):
		self.x = rx
		self.y = ry
		self.source = source
		self.contact = False
	
	def update(self,screen):
		if self.source == 'ENEMY':
			self.y +=5
			color = 0
		else:
			color = 255
			self.y -= 20
		if not self.contact:
			for i in range(0,20):
				pygame.draw.circle(screen, (255,color,255), (self.x, self.y+i),5)
class Blitz:
	def __init__(self, rx, ry, source):
		self.x = rx
		self.y = ry
		self.source = source
		self.contact = False

	def update(self,screen):
		if self.source == 'ENEMY':
			self.y += 5
			color = 0
		else:
			color = 255
			self.y -= 5
		if not self.contact:
			pygame.draw.circle(screen, (255,color,255),(self.x, self.y),5)

class Shield:
	def __init__(self, rx, ry, source):
		self.x = rx
		self.y = ry
		self.source
	
	def update(self, screen):
		pass

