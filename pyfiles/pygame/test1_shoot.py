import pygame
from pygame.locals import *
import sys, math

class Bullet:
	def __init__(self,screen, rx, ry):
		self.x = rx
		self.y = ry
		self.screen = screen
	
	def shoot(self):
		self.y -= 5
		pygame.draw.circle(self.screen, (255,255,255),(self.x, self.y),5)

def main():
	(w,h) = (400,400)
	rx = w/2
	ry = h/2
	flag = 0
	shotflag = 1

	pygame.init()
	pygame.display.set_mode((w,h), 0, 32)
	screen = pygame.display.get_surface()
	im = pygame.image.load("renge.png").convert_alpha()
	rect = im.get_rect()
	rect.center = (rx,ry)

	while True:
		pygame.display.update()
		pygame.time.wait(30)
		screen.fill((0,20,0,0))
		screen.blit(im,rect)

		#key
		pressed_key = pygame.key.get_pressed()
		if pressed_key[K_LEFT]:  rect.move_ip(-1,0); rx-=1
		if pressed_key[K_RIGHT]: rect.move_ip(1,0);  rx+=1
		if pressed_key[K_UP]:    rect.move_ip(0,-1); ry-=1
		if pressed_key[K_DOWN]:  rect.move_ip(0,1);  ry+=1

		#event
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == K_SPACE:
					bullet = Bullet(screen, rx, ry)
					flag = 1
					shotflag = 1
		if flag:
			bullet.shoot()
"""		#shoot
		if flag:
			if shotflag:
				x = rx
				y = ry
				shotflag = 0
			else:
				y -=5

			#keep range
			if y < 0: flag = 0
			pygame.draw.circle(screen, (255,255,255), (x,y), 5)
"""
if __name__ == '__main__':
	main()
