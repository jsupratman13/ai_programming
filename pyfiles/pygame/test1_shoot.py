import pygame
from pygame.locals import *
import sys, math, time

class Player:
	def __init__(self, screen):
		self.image = pygame.image.load("renge.png").convert_alpha()
		self.rect = self.image.get_rect()
		
		#initial player start
		self.rx = screen.centerx/2
		self.ry = screen.centery/2
		self.rect.centery = screen.centery
		self.rect.centerx = screen.centerx

		self.shot_interval = time.time()
		self.shots = []
		self.max_shots = 2

	def key_handler(self, pressed_key):
		if pressed_key[K_LEFT]:  self.rect.move_ip(-1,0);
		if pressed_key[K_RIGHT]: self.rect.move_ip(1,0);
		if pressed_key[K_UP]:    self.rect.move_ip(0,-1);
		if pressed_key[K_DOWN]:  self.rect.move_ip(0,1);
		if pressed_key[K_SPACE]:
		#	if len(self.shots) < self.max_shots:
			if time.time() - self.shot_interval > 1:
				self.shot_interval = time.time()
				self.shots.append(Bullet(self.rect.centerx, self.rect.top))

	def update(self, screen):
		for s in self.shots:
			s.update(screen)

	def show(self, screen):
		screen.blit(self.image, self.rect)

class Bullet:
	def __init__(self, rx, ry):
		self.x = rx
		self.y = ry
	
	def update(self,screen):
		self.y -= 5
		pygame.draw.circle(screen, (255,255,255),(self.x, self.y),5)

def main():
	(w,h) = (800,800)
	rx = w/2
	ry = h/2
	flag = 0
	shotflag = 1

	pygame.init()
	pygame.display.set_mode((w,h), 0, 32)
	screen = pygame.display.get_surface()
	
	player = Player(screen.get_rect())
	while True:
		pygame.display.update()
		pygame.time.wait(30)
		screen.fill((0,20,0,0))

		#key
		pressed_key = pygame.key.get_pressed()
		player.key_handler(pressed_key)
		player.update(screen)
		player.show(screen)
		#event
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
#				if event.key == K_SPACE:
#					bullet = Bullet(screen, rx, ry)
#					flag = 1
#					shotflag = 1
#		if flag:
#			bullet.update()

if __name__ == '__main__':
	main()
