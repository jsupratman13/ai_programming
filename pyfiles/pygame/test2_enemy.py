import pygame
from pygame.locals import *
import sys, math, time

#collision between drawn points and image
def detect_collision(bullet, enemy):
	ex, ey = enemy.rect.centerx, enemy.rect.centery
	e_radiusx = math.fabs(ex - enemy.rect.left)
	e_radiusy = math.fabs(ey - enemy.rect.bottom)
	e_radius = max(e_radiusx, e_radiusy)

	bx, by = bullet.x, bullet.y
	dist = math.hypot(ex-bx, ey-by)
	limit_dist = 5+e_radius
	
	return limit_dist > dist

class Player:
	def __init__(self, screen):
		self.image = pygame.image.load("renge.png").convert_alpha()
		self.rect = self.image.get_rect()
		
		#initial player start
		self.rect.bottom = screen.bottom
		self.rect.centerx = screen.centerx

		self.shot_interval = time.time()
		self.shots = []
		self.max_shots = 2

	def key_handler(self, pressed_key):
		if pressed_key[K_LEFT]:  self.rect.move_ip(-5,0);
		if pressed_key[K_RIGHT]: self.rect.move_ip(5,0);
		if pressed_key[K_UP]:    self.rect.move_ip(0,-5);
		if pressed_key[K_DOWN]:  self.rect.move_ip(0,5);
		if pressed_key[K_SPACE]:
		#	if len(self.shots) < self.max_shots:
			if time.time() - self.shot_interval > 1:
				self.shot_interval = time.time()
				self.shots.append(Bullet(self.rect.centerx, self.rect.top))

	def update(self, screen):
		for s in self.shots:
			s.update(screen)

		screen.blit(self.image, self.rect)

	def hit_target(self, enemy_list):
		for s in self.shots:
			for enemy in enemy_list:
		#	if pygame.sprite.collide_circle(s.current(), enemy):
				if detect_collision(s,enemy):
					enemy.is_alive = False
					s.contact = True

class Enemy:
	def __init__(self,x,y):
		self.image = pygame.image.load("mio.png").convert_alpha()
		self.rect = self.image.get_rect()
		
		self.rect.centerx = x
		self.rect.centery = y

		self.wall_flag = 0
		self.is_alive = True

	def update(self, screen):
		if self.rect.x < 200:
			self.wall_flag = 1
		if self.rect.x > 600:
			self.wall_flag = 0

		if self.wall_flag == 1:
			self.rect.x += 1
		else:
			self.rect.x -= 1
		
		screen.blit(self.image, self.rect)


class Bullet:
	def __init__(self, rx, ry):
		self.x = rx
		self.y = ry
		self.contact = False

	def update(self,screen):
		self.y -= 5
		if not self.contact:
			pygame.draw.circle(screen, (255,255,255),(self.x, self.y),5)

def main():
	(w,h) = (800,800)
	pygame.init()
	pygame.display.set_mode((w,h), 0, 32)
	screen = pygame.display.get_surface()
	
	player = Player(screen.get_rect())

	enemy = Enemy(400,100)
	enemy_list = [enemy]
	respawn = False
	respawn_time = time.time()
	while True:
		pygame.display.update()
		pygame.time.wait(30)
		screen.fill((0,20,0,0))

		#player
		pressed_key = pygame.key.get_pressed()
		player.key_handler(pressed_key)
		player.update(screen)
		
		#enemy
		for e in enemy_list:
			e.update(screen)

		#hit effect
		player.hit_target(enemy_list)
		for enemy in enemy_list:
			if not enemy.is_alive:
				print 'enemy destroyed'
				enemy_list.remove(enemy)

		#respawn enemy
		if not enemy_list and not respawn:
			respawn_time = time.time()
			respawn = True

		if time.time() - respawn_time > 3 and respawn:
			respawn_time = time.time()
			respawn = False
			enemy_list.append(Enemy(400,100))

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
