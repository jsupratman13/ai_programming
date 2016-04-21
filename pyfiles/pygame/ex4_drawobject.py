import pygame
from pygame.locals import *
import sys

def main():
	pygame.init()
	screen = pygame.display.set_mode((300,200))
	pygame.display.set_caption('OBJECT')
	
	while True:
		screen.fill((0,0,0))
		pygame.draw.ellipse(screen, (0,100,0), (50,50,200,100), 5) #draw oval
		pygame.draw.rect(screen, (0,80,0), Rect(10,10,80,50) ,5) #draw rect
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

if __name__ == '__main__':
	main()
