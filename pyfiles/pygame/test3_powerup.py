import pygame
from pygame.locals import *
import sys, math, time,copy

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
		
		#hit point
		self.shot_interval = time.time()
		self.shots = []
		self.max_shots = 2
		self.is_alive = True

		#upgrades
		self.MOVE_SPEED = 2
		self.SHOT_SPEED = 1
		self.LASER_SPEED = 1
		self.WEAPON = 0

	def key_handler(self, pressed_key):
		if pressed_key[K_LEFT]:  self.rect.move_ip(-self.MOVE_SPEED,0);
		if pressed_key[K_RIGHT]: self.rect.move_ip(self.MOVE_SPEED,0);
		if pressed_key[K_UP]:    self.rect.move_ip(0,-self.MOVE_SPEED);
		if pressed_key[K_DOWN]:  self.rect.move_ip(0,self.MOVE_SPEED);
		if pressed_key[K_SPACE]:
			if self.WEAPON == 0:
			#	if len(self.shots) < self.max_shots:
				if time.time() - self.shot_interval > self.SHOT_SPEED:
					self.shot_interval = time.time()
					self.shots.append(Bullet(self.rect.centerx, self.rect.top, 'PLAYER'))
			if self.WEAPON == 1:
				if time.time() - self.shot_interval < self.LASER_SPEED:
					self.shots.append(Laser(self.rect.centerx, self.rect.top, 'PLAYER'))
				elif time.time() - self.shot_interval > self.LASER_SPEED*2:
					self.shot_interval = time.time()

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
		self.shots = []
		self.shot_interval = time.time()

	def update(self, screen):
		if self.rect.x < 200:
			self.wall_flag = 1
		if self.rect.x > 600:
			self.wall_flag = 0

		if self.wall_flag == 1:
			self.rect.x += 1
		else:
			self.rect.x -= 1
	
		if time.time() - self.shot_interval > 3:
			self.shot_interval = time.time()
			self.shots.append(Bullet(self.rect.centerx, self.rect.bottom, 'ENEMY'))	
		for s in self.shots:
			s.update(screen)

		screen.blit(self.image, self.rect)
	
	def hit_target(self, player_list):
		for s in self.shots:
			for player in player_list:
				if detect_collision(s, player):
					player.is_alive = False
					s.contact = True

class Bullet:
	def __init__(self, rx, ry, source):
		self.x = rx
		self.y = ry+5
		self.source = source
		self.contact = False

	def update(self,screen):
		if self.source == 'ENEMY':
			self.y += 5
			color = 0
		else:
			color = 255
			self.y -= 5
		if not self.contact:
			pygame.draw.circle(screen, (255,color,255),(self.x, self.y),5)

class Laser:
	def __init__(self, rx, ry, source):
		self.x = rx
		self.y = ry
		self.source = source
		self.contact = False
	
	def update(self,screen):
		if self.source == 'ENEMY':
			self.y +=5
			color = 0
		else:
			color = 255
			self.y -= 5
		if not self.contact:
			pygame.draw.circle(screen, (255,color,255), (self.x, self.y),5)
			
class Powerup:
	def __init__(self, screen):
		self.powerup = [Powerup.RapidPowerup(screen), \
				Powerup.SpeedPowerup(screen), \
				Powerup.LaserWeapon(screen)]

	def update(self, player_list):
		for p in self.powerup:
			for player in player_list:
				if detect_collision(p, player):
					p.contact = True	
				p.update()

	class RapidPowerup:
		def __init__(self, screen):
			self.screen = screen
			self.contact = False
			self.x = 250
			self.y = 600
			self.UPDATE = 0.5
		
		def update(self, player):
			if not self.contact:
				pygame.draw.circle(self.screen, (255,0,0),(self.x, self.y),10)
			else:	
				player.SHOT_SPEED = self.UPDATE		

	class SpeedPowerup:
		def __init__(self,screen):
			self.screen = screen
			self.contact = False
			self.x = 650
			self.y = 600
			self.UPDATE = 5
	
		def update(self, player):
			if not self.contact:
				pygame.draw.circle(self.screen, (0,0,255),(self.x, self.y), 10)
			else:
				player.MOVE_SPEED = self.UPDATE

	class LaserWeapon:
		def __init__(self,screen):
			self.screen = screen
			self.contact = False
			self.x = 700
			self.y = 700
			self.UPDATE = 1

		def update(self, player):
			if not self.contact:
				pygame.draw.circle(self.screen, (0,255,0),(self.x, self.y),10)
			else:
				player.WEAPON = self.UPDATE
class Game:
	def __init__(self):
		(w,h) = (800,800)
		pygame.init()
		pygame.display.set_mode((w,h), 0, 32)
		self.screen = pygame.display.get_surface()
		
		self.player = Player(self.screen.get_rect())
		self.player_list = [self.player]		

		self.enemy = Enemy(400,100)
		self.enemy_list = [self.enemy]

		self.respawn = False
		self.respawn_time = time.time()

		self.power_up = Powerup(self.screen)

	def main(self):
		pygame.display.update()
		pygame.time.wait(30)
		self.screen.fill((0,20,0,0))
		pressed_key = pygame.key.get_pressed()
		
		#player
		for p in self.player_list:
			p.key_handler(pressed_key)
			p.update(self.screen)
			p.hit_target(self.enemy_list)
			if not p.is_alive:
				print 'player destroyed'
				self.player_list.remove(p)
		
		#enemy
		for e in self.enemy_list:
			e.update(self.screen)
			e.hit_target(self.player_list)
			if not e.is_alive:
				print 'enemy destroyed'
				self.enemy_list.remove(e)

		#respawn enemy
		if not self.respawn and (not self.enemy_list or not self.player_list):
			self.respawn_time = time.time()
			self.respawn = True

		if time.time() - self.respawn_time > 3 and self.respawn:
			self.respawn_time = time.time()
			self.respawn = False
			if not self.enemy_list:
				self.enemy_list.append(Enemy(400,100))
			if not self.player_list:
				self.player_list.append(Player(self.screen.get_rect()))

		#powerup
		self.power_up.update(self.player_list)

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
	game = Game()
	while True:
		game.main()
