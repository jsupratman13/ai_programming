import numpy as np
import pygame
from pygame.math import Vector2
import sys,time,copy
import random, math

class WorldMap(object):
    def __init__(self):
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.GREEN = (0,255,0)
        self.RED = (255,0,0)
        self.BLUE = (0,0,255)
        self.PURPLE = (255,0,255)
        self.YELLOW = (255,255,0,)

        self.MARGIN = 5
        self.HEIGHT = 350
        self.WIDTH = self.HEIGHT
        self.WINDOW_SIZE = []
        
        self.landmarks = []
        for i in range(3):
            x, y = random.randint(self.MARGIN+5, self.WIDTH/2-self.MARGIN-5),random.randint(self.MARGIN+5, self.HEIGHT-self.MARGIN-5)
            self.landmarks.append([x,y])

        self.WORLD = pygame.Rect([self.MARGIN, self.MARGIN, self.HEIGHT-self.MARGIN, self.WIDTH-self.MARGIN])
    
    def get_landmarks(self,pose):
        positions = []
        x,y,th = pose
        for i,landmark in enumerate(self.landmarks):
            lx,ly = landmark[0],landmark[1]
            distance = math.sqrt((x-lx)**2 + (y-ly)**2)
            direction = math.atan2(ly-y, lx-x) - th
            positions.append([distance,direction,lx,ly,i])
        return positions

    def draw(self):
        for l in self.landmarks:
            pygame.draw.circle(screen, self.GREEN, (l[0],l[1]),5)

    def fit_window_to_grid(self):
        WIDTH = self.WIDTH
        HEIGHT = self.HEIGHT
        self.WINDOW_SIZE = [WIDTH, HEIGHT]
        return self.WINDOW_SIZE

class PacMan(object):
    def __init__(self, pose, WORLD_SIZE=350, WIDTH=350):
        self.pose = pose
        self.movement_noise = [0.1, math.pi/180.0*3.0] #translate noise
        self.rotation_noise = 0.1
        self.sense_noise = [0.1, 5.0/180*math.pi] #distance, direction sense noise
    
    def estimated_motion(self, pos, move, rotate):
        move = random.gauss(move, move*self.movement_noise[0])
        dir_error = random.gauss(0.0, self.movement_noise[1])
        px,py,pt = pos
        x = px + move * math.cos(pt+dir_error)
        y = py + move * math.sin(pt+dir_error)
        th = pt + dir_error + random.gauss(rotate, rotate*self.rotation_noise)
        th = clamp_rad(th) 
        return [x, y, th]

    def estimated_observation(self, m):
        measurements = m.get_landmarks(self.pose)
        observations = []
        for m in measurements:
            distance, direction, lx, ly, i = m
            if math.cos(direction) < 0.0: continue
            measured_distance = random.gauss(distance, distance*self.sense_noise[0])
            measured_direction = random.gauss(direction, self.sense_noise[1])
            observations.append([measured_distance, measured_direction, lx, ly, i])
            pygame.draw.line(screen, RED, (lx,ly), (self.pose[0], self.pose[1]))
        return observations

class LandmarkEstimation():
    def __init__(self):
        self.pos = np.array([[0.0],[0.0]])
        self.cov = np.array([[1000000000.0**2, 0.0],[0.0,1000000000.0**2]])

class Particle(object):
    def __init__(self, pose, w):
        self.w = w
        self.pose = pose
        self.map = [LandmarkEstimation(), LandmarkEstimation(), LandmarkEstimation()]

    def motion_update(self, move, rotate, agent):
        self.pose = agent.estimated_motion(self.pose, move, rotate)

    def measurement_update(self, measurement):
        x,y,th = self.pose
        distance, direction ,lx, ly, i = measurement
        ln = self.map[i]
        lx = x + distance*math.cos(th+direction)
        ly = y + distance*math.sin(th+direction)

        delta = np.array([[x],[y]])-np.array([[lx],[ly]])
        coef = 2 * math.pi * math.sqrt(np.linalg.det(ln.cov))
        inexp = -0.5 * (delta.T.dot(np.linalg.inv(ln.cov))).dot(delta)
        self.w *= 1.0/coef*math.exp(inexp)
        
        z = np.array([[lx],[ly]])
        c = math.cos(th+direction)
        s = math.sin(th+direction)
        rot = np.array([[c,s],[-s,c]])

        err_agent = np.array([[(distance*0.1)**2,0.0],[0.0,(distance*math.sin(5.0/180.*math.pi))**2]])
        err_world = (rot).dot(err_agent).dot((rot.T))

        ln.cov = np.linalg.inv(np.linalg.inv(ln.cov)+np.linalg.inv(err_world))
        K = (ln.cov).dot(np.linalg.inv(err_world))
        ln.pos += K.dot(z-ln.pos)

    def draw_landmark(self, i):
        WIDTH = 350*4
        HEIGHT = 350*4
        for e in self.map:
            eigen_vals, eig_vec = np.linalg.eig(e.cov)
            v1 = eigen_vals[0] * eig_vec[:,0]
            v2 = eigen_vals[1] * eig_vec[:,1]
            v1_direction = math.atan2(v1[1], v1[0])
            x,y = e.pos
            width = max(20, min(WIDTH,10*math.sqrt(np.linalg.norm(v1))))
            height = max(20, min(HEIGHT, 10*math.sqrt(np.linalg.norm(v2))))
            ellip = pygame.Rect(0,0,width,height)
            ellip.centerx,ellip.centery = x, y
            pygame.draw.ellipse(screen, BLUE, ellip)

    def draw_pos(self):
        pygame.draw.circle(screen,(255,0,255) , (int(self.pose[0]),int(self.pose[1])), 3)

class FastSLAM(object):
    def __init__(self, pose, particle_num=100):
        self.N = particle_num
        self.particles = [Particle(pose,1.0/self.N) for i in range(self.N)]
    
    def draw(self):
        for (i,p) in enumerate(self.particles):
            #p.draw_pos()
            p.draw_landmark(i)
            if i > 3: return
    
    def motion_update(self, move, rotate, agent):
        for p in self.particles:
            p.motion_update(move, rotate, agent)
    
    def measurement_update(self, measurement):
        for p in self.particles:
            p.measurement_update(measurement)
        self.resampling()

    def resampling(self):
        ws = [e.w+1e-100 for e in self.particles]
        sample = []
        pointer = 0.0
        index = int(random.random()*self.N)
        max_w = max(ws)
        for i in range(self.N):
            pointer += random.uniform(0, 2*max_w)
            while ws[index] < pointer:
                pointer -= ws[index]
                index = (index+1)%self.N
            self.particles[index].weight = 1.0/self.N
            sample.append(copy.deepcopy(self.particles[index]))
        self.particles = sample

def clamp_rad(th):
    return th%(2*math.pi)
    
if __name__ == '__main__':
    #initialize world
    world = WorldMap()
    
    BLACK = world.BLACK
    WIDTH = world.WIDTH
    HEIGHT = world.HEIGHT
    MARGIN = world.MARGIN
    RED = world.RED
    BLUE = world.BLUE
    
    pygame.init()
    
    WINDOW_SIZE = world.fit_window_to_grid()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("wandering pacman")
    clock = pygame.time.Clock()

    #initialize images and place image at random location
    im_org = pygame.image.load('pacman.png').convert_alpha()
    im_org = pygame.transform.scale(im_org, (50,50))
    im = im_org.copy()
    rect = im_org.get_rect()
    init_x = random.randint(MARGIN+rect.width, WIDTH-(MARGIN+rect.width))
    init_y = random.randint(MARGIN+rect.height, HEIGHT-(MARGIN+rect.height))
    rect.center = (init_x,init_y)
    
    #initialize agent and slam
    pacman = PacMan([init_x,init_y, 0])
    slam = FastSLAM(pacman.pose)
    angle = 0
    direction = Vector2(1,0)
    pos = Vector2(rect.center)
    speed = 0
    angle_speed = 0

    while True:
        #display event
        pygame.display.update()
        clock.tick(60)
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                update_flag = True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        #key event
        pressed_key = pygame.key.get_pressed()
        angle_speed = 0
        speed = 0
        if pressed_key[pygame.K_LEFT]: 
            angle_speed = -4.0
        if pressed_key[pygame.K_RIGHT]:
            angle_speed = 4.0
        if pressed_key[pygame.K_UP]: 
            speed = 2.0
        if pressed_key[pygame.K_DOWN]:
            speed = -2.0

        #update pacman position
        if angle_speed != 0:
            direction.rotate_ip(angle_speed)
            angle += angle_speed
            im = pygame.transform.rotate(im_org, -angle)
            rect = im.get_rect(center=rect.center)
        pos += direction * speed
        rect.center = pos

        #fast slam
        if speed != 0 or angle_speed != 0:
            slam.motion_update(speed, math.radians(angle_speed), pacman)
            pacman.pose = [rect.centerx, rect.centery, clamp_rad(math.radians(angle))]
            observations = pacman.estimated_observation(world)
            for m in observations:
                slam.measurement_update(m)
        
        #draw
        slam.draw()
        world.draw()
        screen.blit(im,rect)
        

