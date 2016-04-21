import pygame
from pygame.locals import *
import sys

def main():
	pygame.init()
	screen = pygame.display.set_mode((300,200))
	pygame.display.set_caption("GAME")
	font = pygame.font.Font(None, 55) 	#font setup 55px

	while True:
		screen.fill((0,0,0))
		text = font.render("TEST", True, (255,255,255)) 	#text setup
		screen.blit(text, [20,100])	#view text location
		pygame.display.update()

		for event in pygame.event.get():
			if event.type ==QUIT:
				pygame.quit()
				sys.exit()

if __name__ == '__main__':
	main()
