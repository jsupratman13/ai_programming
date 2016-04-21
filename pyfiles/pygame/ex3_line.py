import pygame
from pygame.locals import *
import sys

def main():
	pygame.init()
	screen = pygame.display.set_mode((300,200))
	pygame.display.set_caption('LINE')
	
	while True:
		screen.fill((255,255,255))
		pygame.draw.line(screen, (0,95,0), (0,0), (80,80), 5) #draw line
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

if __name__ == '__main__':
	main()
