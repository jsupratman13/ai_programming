import pygame
from pygame.locals import * 
import sys

def main():
	(w,h) = (400,400)
	(x,y) = (w/2, h/2)
	pygame.init()
	pygame.display.set_mode((w,h), 0,32) 	#setup display
	screen = pygame.display.get_surface()	#pull surface
	
	player = pygame.image.load("player.jpg").convert_alpha()	#load char
	player = pygame.transform.scale(player, (25,25))
	rect_player = player.get_rect()	#grab char
	rect_player.center = (300,200)	#set char center
	bg = pygame.image.load("bg.jpg").convert_alpha()	#load bg
	rect_bg = bg.get_rect()	#grab bg

	while True:
		pygame.display.update()
		pygame.time.wait(30)	#time wait/update interval
		screen.fill((0,20,0,0))
		screen.blit(bg, rect_bg)	#display bg start from bg to top
		screen.blit(player, rect_player)	#display char

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

