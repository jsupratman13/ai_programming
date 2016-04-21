import pygame
from pygame.locals import * 
import sys

def main():
	(w,h) = (400,400)
	pygame.init()
	pygame.display.set_mode((w,h), 0,32) 	#setup display
	screen = pygame.display.get_surface()	#pull surface
	bg = pygame.image.load("bg.jpg").convert_alpha()	#load background
	rect_bg = bg.get_rect()	#grab rectangle

	while True:
		pygame.display.update()
		pygame.time.wait(30)	#time wait/update interval
		screen.fill((0,20,0,0))
		screen.blit(bg,rect_bg)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == KEYDOWN:	#if key pressed
				if event.key == K_ESCAPE:	#if escape key pressed
					pygame.quit()
					sys.exit()

if __name__ == '__main__':
	main()

