import pygame
from pygame.locals import *
import sys

def main():
	(w,h) = (400,400)
	(x,y) = (w/2, h/2)
	pygame.init()
	pygame.display.set_mode((w,h), 0, 32)
	screen = pygame.display.get_surface()
	im = pygame.image.load('renge.png').convert_alpha()
	rect = im.get_rect()
	rect.center = (w/2, h/2)

	while True:
		pygame.display.update()
		pygame.time.wait(30)
		screen.fill((0,20,0,0))

		screen.blit(im, rect)
		
		#key
		pressed_key = pygame.key.get_pressed()
		if pressed_key[K_LEFT]:  rect.move_ip(-1,0)
		if pressed_key[K_RIGHT]: rect.move_ip(1,0)
		if pressed_key[K_UP]:    rect.move_ip(0,-1)
		if pressed_key[K_DOWN]:  rect.move_ip(0,1)

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
	main()
