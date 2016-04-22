import pygame
from pygame.locals import *
import time,math
from weapons import Bullet, Laser

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

def danger_zone(bullet, player, dist):
	ex, ey = player.centerx, player.centery
	e_radiusx = math.fabs(ex - player.left)
	e_radiusy = math.fabs(ey - player.bottom)
	e_radius = max(e_radiusx, e_radiusy)

	bx, by = bullet.x, bullet.y
	current_dist = math.hypot(ex-bx, ey-by)
	limit_dist = dist+5+e_radius
	
	return limit_dist > current_dist

def shot_range(enemy, player, dist):
	ex, ey = player.centerx, player.centery
	e_radiusx = math.fabs(ex - player.left)
	e_radiusy = math.fabs(ey - player.bottom)
	e_radius = max(e_radiusx, e_radiusy)

	bx, by = enemy.center.x, enemy.center.y

	current_dist = math.hypot(ex-bx, ey-by)
	limit_dist = dist+e_radius
	
	return limit_dist > current_dist

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
		self.LASER_SPEED = 0.5
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
				elif time.time() - self.shot_interval > self.LASER_SPEED*5:
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

	def update(self, screen, player_list):
		dodge_flag = False
		for player in player_list:
			px = player.rect.centerx
			py = player.rect.centery
			#dodge
			for s in player.shots:
				if danger_zone(s, self.rect, 50) or dodge_flag:
					dodge_flag = True
					if self.rect.centerx > 790 or self.rect.centerx < 10:
						pass
					elif s.x > self.rect.centerx:
						if player.WEAPON == 1:
							self.rect.x -= 5
						else:
							self.rect.x -= 3
					else:
						if player.WEAPON == 1:
							self.rect.x += 5
						else:
							self.rect.x += 3

					if self.rect.centery < 10:
						pass
					elif s.y > self.rect.centery and math.fabs(s.y-self.rect.centery) < 70:	
						self.rect.y -= 3
					
				#	if danger_zone(s, self.rect, 100):
					if math.fabs(s.x - self.rect.x) > 50:
						dodge_flag = False
				else:
	
					if math.fabs(py-self.rect.centery) > 500:
						self.rect.y += 3
					elif math.fabs(py-self.rect.centery) < 100:
						self.rect.y -= 3
			
					if math.fabs(px-self.rect.centerx) > 20:
						if px > self.rect.centerx:
							self.rect.x += 3
						else:
							self.rect.x -= 3
					else:
						if time.time() - self.shot_interval > 2:
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
