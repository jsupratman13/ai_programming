import pygame
from pygame.locals import *
import sys

def main():
	pygame.init()	#initalize pygame
	screen = pygame.display.set_mode((400,300))	#set size
	pygame.display.set_caption("Test")	#set title

	while True:
		screen.fill((200,200,200))	#color
		pygame.display.update()	#update display loop

		for event in pygame.event.get():
			if event.type == QUIT:	#when quit button is pressed
				pygame.quit()	#finish pygame
				sys.exit()

if __name__ == '__main__':
	main()
