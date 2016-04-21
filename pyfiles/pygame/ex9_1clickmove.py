import pygame
from pygame.locals import *
import sys

def main():
	(w,h) = (400,400)
	(x,y) = (w/2, h/2)

	pygame.init()
	pygame.display.set_mode((w,h), 0, 32)
	screen = pygame.display.get_surface()
	player = pygame.image.load("renge.png").convert_alpha()

	while True:
		pygame.display.update()
		pygame.time.wait(30)
		screen.fill((0,20,0,0))
		screen.blit(player, (x,y))

		for event in pygame.event.get():
			#mouse click
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				x,y = event.pos
				x -= player.get_width()/2
				y -= player.get_width()/2

			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()

if __name__ == '__main__':
	main()
