import pygame
from pygame.locals import *
import time,math, random
from weapons import Bullet, Laser

#clamp function
def clamp(value, high, low):
	if value > high:
		value = high
	elif value < low:
		value = low
	return value

#convert x,y to angle
def pos_to_theta(x,y):
	th = math.atan2(y,x)
	return int(math.degrees(th))

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

#minimum area to dodge attack
def danger_zone(bullet, player, dist):
	ex, ey = player.centerx, player.centery
	e_radiusx = math.fabs(ex - player.left)
	e_radiusy = math.fabs(ey - player.bottom)
	e_radius = max(e_radiusx, e_radiusy)

	bx, by = bullet.x, bullet.y
	current_dist = math.hypot(ex-bx, ey-by)
	limit_dist = dist+5+e_radius
	
	return limit_dist > current_dist

class Player:
	def __init__(self, screen):
		self.image = pygame.image.load("renge.png").convert_alpha()
		self.rect = self.image.get_rect()
		
		#initial player start
		self.rect.centery = screen.centery
		self.rect.centerx = screen.centerx
		
		#hit point
		self.shot_interval = time.time()
		self.shots = []
		self.max_shots = 2
		self.is_alive = True

		#upgrades
		self.MOVE_SPEED = 5
		self.SHOT_SPEED = 1
		self.LASER_SPEED = 0.5
		self.WEAPON = 0

	def key_handler(self, pressed_key, mouse_event):
		#User Movement
		x,y = mouse_event.get_pos()
		b1, b2, b3 = mouse_event.get_pressed()
		angle = pos_to_theta(self.rect.centery-y,self.rect.centerx-x)
#		angle = -90
		old_center = self.rect.center
		self.image_rotate = pygame.transform.rotate(self.image, angle)
		self.rect_rotate = self.image_rotate.get_rect(center = old_center)

		if pressed_key[K_a]:  
			self.rect.x += -self.MOVE_SPEED*math.cos(math.radians(angle))
			self.rect.y +=  self.MOVE_SPEED*math.sin(math.radians(angle))
		if pressed_key[K_d]: 
			self.rect.x +=  self.MOVE_SPEED*math.cos(math.radians(angle))
			self.rect.y += -self.MOVE_SPEED*math.sin(math.radians(angle))
		if pressed_key[K_w]:
			self.rect.x += -self.MOVE_SPEED*math.sin(math.radians(angle))
			self.rect.y += -self.MOVE_SPEED*math.cos(math.radians(angle))
		if pressed_key[K_s]:  
			self.rect.x +=  self.MOVE_SPEED*math.sin(math.radians(angle))
			self.rect.y +=  self.MOVE_SPEED*math.cos(math.radians(angle))

		if b1:
#			if len(self.shots) < self.max_shots:
			if time.time() - self.shot_interval > self.SHOT_SPEED:
				self.shot_interval = time.time()
				self.shots.append(Bullet(self.rect_rotate, angle, 'PLAYER'))

	def update(self, screen):
		for s in self.shots:
			s.update(screen)
		self.rect.x = clamp(self.rect.x, 740, 10)
		self.rect.y = clamp(self.rect.y, 740, 10)
		screen.blit(self.image_rotate, self.rect_rotate)

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

		#initial position
		self.rect.centerx = x
		self.rect.centery = y

		#parameters
		self.wall_flag = 0
		self.is_alive = True
		self.shots = []
		self.shot_interval = time.time()

		self.current_time = time.time()
		self.RANDOM = random.randint(1,3)
		self.flag_left = True

		self.MOVE_SPEED = 5	

		#Initialize FSM
		self.state_list ={'DODGE':self.DodgeState, \
				  'APPROACH': self.ApproachState, \
				  'SHOOT': self.ShootState, \
				  'IDLE': self.IdleState, \
				  'MOVE': self.MoveState, \
				  'DODGESHOOT': self.DodgeShootState }
		self.player_list = []
		self.transition = 'MOVE'
		self.initial_transition = None

	def IdleState(self):
		for player in self.player_list:
			px = player.rect.centerx
			py = player.rect.centery		
			angle = pos_to_theta(self.rect.centery-py, self.rect.centerx-px)
			old_center = self.rect.center
			self.image_rotate = pygame.transform.rotate(self.image, angle)
			self.rect_rotate = self.image_rotate.get_rect(center = old_center)
			if time.time() - self.shot_interval > 2:
				self.shot_interval = time.time()
				self.shots.append(Bullet(self.rect_rotate, angle, 'ENEMY'))

	def DodgeShootState(self):
		dodge_list = []
		for player in self.player_list:
			px = player.rect.centerx
			py = player.rect.centery
			for s in player.shots:
				if danger_zone(s, self.rect, 80):
					angle = pos_to_theta(self.rect.centery-s.y, self.rect.centerx-s.x)

					if angle > 0: self.flag_left = True
					else: self.flag_left = False

					if self.flag_left:  
						self.rect.x += -self.MOVE_SPEED*math.cos(math.radians(angle))
						self.rect.y +=  self.MOVE_SPEED*math.sin(math.radians(angle))
					else: 
						self.rect.x +=  self.MOVE_SPEED*math.cos(math.radians(angle))
						self.rect.y += -self.MOVE_SPEED*math.sin(math.radians(angle))
					break
			else:
				self.transition = 'MOVE'
					
			angle = pos_to_theta(self.rect.centery-py, self.rect.centerx-px)
			old_center = self.rect.center
			self.image_rotate = pygame.transform.rotate(self.image, angle)
			self.rect_rotate = self.image_rotate.get_rect(center = old_center)

			if time.time() - self.shot_interval > 2:
				self.shot_interval = time.time()
				self.shots.append(Bullet(self.rect_rotate, angle, 'ENEMY'))
						
	def MoveState(self):
		for player in self.player_list:
			for s in player.shots:
				if danger_zone(s, self.rect, 80):
					self.transition = 'DODGESHOOT'
			px = player.rect.centerx
			py = player.rect.centery
			angle = pos_to_theta(self.rect.centery-py, self.rect.centerx-px)			

			old_center = self.rect.center
			self.image_rotate = pygame.transform.rotate(self.image,angle)
			self.rect_rotate = self.image_rotate.get_rect(center = old_center)

			if self.flag_left:  
				self.rect.x += -self.MOVE_SPEED*math.cos(math.radians(angle))
				self.rect.y +=  self.MOVE_SPEED*math.sin(math.radians(angle))
			else: 
				self.rect.x +=  self.MOVE_SPEED*math.cos(math.radians(angle))
				self.rect.y += -self.MOVE_SPEED*math.sin(math.radians(angle))


#			if self.flag_approach == 1:
#				self.rect.x += -self.MOVE_SPEED*math.sin(math.radians(angle))
#				self.rect.y += -self.MOVE_SPEED*math.cos(math.radians(angle))
#			elif self.flag_approach == 2:  
#				self.rect.x +=  self.MOVE_SPEED*math.sin(math.radians(angle))
#				self.rect.y +=  self.MOVE_SPEED*math.cos(math.radians(angle))

			if time.time() - self.current_time > self.RANDOM:
				self.flag_left = False if self.flag_left else True
				self.current_time = time.time()
				self.RANDOM = random.randint(1,3)				

			if time.time() - self.shot_interval > 2:
				self.shot_interval = time.time()
				self.shots.append(Bullet(self.rect_rotate, angle, 'ENEMY'))
			
	def DodgeState(self):
		dodge_list = []
		for player in self.player_list:
			px = player.rect.centerx
			py = player.rect.centery
			for s in player.shots:
				if danger_zone(s, self.rect, 80) and s.y > self.rect.centery:
					dodge_list.append(s)
			
			for s in dodge_list:
				if self.rect.centerx > 750 or self.rect.centerx < 50:
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
				elif math.fabs(s.y-self.rect.centery) < 70:
					self.rect.y -= 3
			if not dodge_list:
				self.transition = 'APPROACH'

	def ApproachState(self):
		for player in self.player_list:
			px = player.rect.centerx
			py = player.rect.centery
			for s in player.shots:
				if danger_zone(s, self.rect, 80) and s.y > self.rect.centery:
					self.transition = 'DODGE'
			else:
				if math.fabs(px-self.rect.centerx) > 25:
					if px > self.rect.centerx:
						self.rect.x += 3
					else:
						self.rect.x -= 3
				elif math.fabs(py - self.rect.centery) > 500:
					self.rect.y += 3
				elif math.fabs(py - self.rect.centery) < 100:
					self.rect.y -= 3
				else:
					self.transition = 'SHOOT'

	def ShootState(self):
		for player in self.player_list:
			px = player.rect.centerx
			for s in player.shots:
				if danger_zone(s, self.rect, 80) and s.y >  self.rect.centery:
					self.transition = 'DODGE'
			else:
				if math.fabs(px - self.rect.centerx) < 30:
					if time.time() - self.shot_interval > 2:
						self.shot_interval = time.time()
						self.shots.append(Bullet2(self.rect.centerx, self.rect.bottom, 'ENEMY'))
				else:
					self.transition = 'APPROACH'

	def update(self, screen, player_list):
		self.player_list = player_list
		self.state_list[self.transition]()
		if self.initial_transition != self.transition:
			print str(self.transition)
			self.initial_transition = self.transition
		for s in self.shots:
			s.update(screen)

		self.rect.x = clamp(self.rect.x, 740, 10)
		self.rect.y = clamp(self.rect.y, 740, 10)
		screen.blit(self.image, self.rect)
	
	def hit_target(self, player_list):
		for s in self.shots:
			for player in player_list:
				if detect_collision(s, player):
					player.is_alive = False
					s.contact = True
