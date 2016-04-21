import pygame
from pygame.locals import *
import sys

def main():
	(w,h) = (400,400)
	(x,y) = (w/2, h/2)
	pygame.init()
	pygame.display.set_mode((w,h), 0, 32)
	screen = pygame.display.get_surface()

	while True:
		pygame.display.update()
		pygame.time.wait(30)
		screen.fill((0,20,0,0))

		#keep range
		if x < 0: x=0
		if x > w: x=w
		if y < 0: y=0
		if y > h: y=h

		#draw circle
		pygame.draw.circle(screen, (0,200,0), (x,y),5)

		#key
		pressed_key = pygame.key.get_pressed()
		if pressed_key[K_LEFT]:  x-=1
		if pressed_key[K_RIGHT]: x+=1
		if pressed_key[K_UP]:    y-=1
		if pressed_key[K_DOWN]:  y+=1

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
