# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 02:49:27 2020

@author: Danny
"""

import pygame, sys, math, random

## Colours
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
ORANGE = [255, 128, 0]
YELLOW = [242, 224, 63]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
LIGHT_BLUE = [0,  255]
PINK = [255, 153, 255]
LIME = [128, 255, 0]

rand_col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

agent_width = 8
agent_height = 20

## Subtract two vectors:
def subtract(a, b):
    
    new_vec = []
    for i in range(len(a)):
        new_vec.append(a[i] - b[i])
    
    return new_vec
        
## Return magnitude, direction of a given vector
def magDir(x, y):
    return math.sqrt(x**2 + y**2), round(math.atan2(y, x), 5)

## Return x, y components of given vector
def resolve(mag, t):
    return mag*math.cos(t), mag*math.sin(t)

## Return direction of given vector
def direction(x, y):
    
    if x == 0.0 or y == 0.0:
        if y > 0:
            return math.pi/2
        else:
            
            return math.pi/2 - math.pi
    
    if x < 0:
        return math.atan(y/x) - math.pi

    else:
        return  math.atan(y/x)

## Return magnitude of given vector
def mag(x, y):
    return math.sqrt(x**2 + y**2)

## Scale given vector to given magnitude
def setMag(x, y, m):
    
    magnitude = mag(x, y)
    
    if magnitude == 0:
        return 0, 0
    else:
    
        x = x/magnitude * m
        y = y/magnitude * m
    
    return x, y

## Scale given vector to unit length
def unitVector(x, y):
    x, y = setMag(x, y, 1)
    
    return x, y

## Limit given vector to given max length
def limit(x, y, a):
    if mag(x, y) >= a:
        x, y = setMag(x, y, a)
        
    return x, y

def distance(body1, body2):
    ## Difference in x-pos and y-pos
    delta_x = body2[0] - body1[0]
    delta_y = body2[1] - body1[1]

    
    ## Uses Pythagorean Theorem
    return math.sqrt((delta_x)**2 + (delta_y)**2)

def rotate(origin, point, angle):

    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def triangleCentroid(points):
    xtot = 0
    ytot = 0
    
    for i in points:
        xtot += i[0]
        ytot += i[1]
        
    return (xtot/3, ytot/3)

## x1, x2 = min, max of original range
## y1, y2 = min, max of new range
## n = original value to convert
def changeRange(min1, max1, min2, max2, n):
    p = min2+(max2-min2)*((n-min1)/(max1-min1))
    return p

class Agent(object):
    def __init__(self, col, p, v, a, f, max_speed, max_force):
        self.col = col
        self.mass = 1
        
        self.px = p[0]
        self.py = p[1]
        
        self.vx = v[0]
        self.vy = v[1]
        
        self.ax = a[0]
        self.ay = a[1]
        
        self.fx = f[0]
        self.fy = f[1]
        
        self.max_speed = max_speed
        self.max_force = max_force
        
        self.width = agent_width
        self.height = agent_height
        
        self.triPoints = [
                [self.px, self.py],
                [self.px-self.width, self.py+self.height],
                [self.px+self.width, self.py+self.height]
                ]
        
        self.target = None
        self.currentAngle = 0
        
    def changePos(self):
        
        self.px = int(self.px + self.vx)
        self.py = int(self.py + self.vy)
    
    def changeVel(self):
        self.vx += self.ax
        self.vy += self.ay
        
    def changeAcc(self):
        self.ax += self.fx/self.mass
        self.ay += self.fy/self.mass
    
    def applyForce(self, force):
        self.fx += force[0]
        self.fy += force[1]
        
    def move(self):
        self.changeAcc()
        self.changeVel()
        self.changePos()
        
        self.triPoints = [
                [self.px, self.py],
                [self.px-self.width, self.py+self.height],
                [self.px+self.width, self.py+self.height]
                ]
        
        angle = direction(self.steer[0], self.steer[1])
        
        if angle == None:
            angle = self.currentAngle
        
        self.currentAngle = angle        
        
        centroid = triangleCentroid(self.triPoints)
        
        angle = direction(self.vx, self.vy) + math.pi/2
        
        for i in self.triPoints:
            i[0], i[1] = rotate(centroid, i, angle)
    
    def lineToCentre(self):
        ## screen, colour, start pos, end pos, width
        pygame.draw.line(screen, WHITE, (self.px, self.py), centre, 2)
    
    ## Bounce off walls of screen
    def bounce(self):
        if self.px + self.vx >= win_size[0] or self.px + self.vx < 0:
            self.vx = -self.vx
            
        if self.py + self.vy >= win_size[1] or self.py + self.vy < 0:
            self.vy = -self.vy
    
    def draw(self):
        
        
        pygame.draw.polygon(screen, self.col,
                        self.triPoints
                        )
        
    def seekTarget(self, target):
        
        if isinstance(target, Agent) == True:
            target = [target.px, target.py]

        desired = subtract(target, (self.px, self.py))
        desired[0], desired[1] = setMag(desired[0], desired[1], self.max_speed)

        
        self.steer = subtract(desired, (self.vx, self.vy))
                
        self.steer[0], self.steer[1] = limit(self.steer[0], self.steer[1], self.max_force)
        
        self.applyForce(self.steer)
        
    def arrive(self):
        self.vx = changeRange(0, target_radius, 0, self.max_speed, self.vx)
        self.vy = changeRange(0, target_radius, 0, self.max_speed, self.vy)
        
        print (self.vx, self.vy)

class Runner(Agent):
    def __init__(self, path_radius, p, v, origin):
        self.path_radius = path_radius
        
        self.px = p[0]
        self.py = p[1]
        
        self.vx = v[0]
        self.vy = v[1]
        
        self.origin = origin
        
        self.t = 0
        
        super().__init__(BLUE, p, v, (0,0), (0,0), 10, 0)
    
    def move(self):
        
        self.px = self.origin[0] + (self.path_radius * math.cos(self.t))
        self.py = self.origin[1] + (self.path_radius * math.sin(self.t))
        
        print (self.px, self.py)
        
    def draw(self):
        pygame.draw.circle(screen, self.col, (int(self.px), int(self.py)), 20)

## Setting window size, defining screen
win_size = (900, 900)
screen = pygame.display.set_mode(win_size)

## Defining centre of screen
centre = (int(win_size[0]/2), int(win_size[1]/2))

## Initialise window
pygame.init()

## Defining clock object
clock = pygame.time.Clock()

agents = []
target_radius = 100
ang_speed = 0.04

for i in range(5):
    a = Agent(WHITE, (random.randint(100, 800), random.randint(100, 800)),
              (0, 0), (0, 0), (0, 0), 10, 0.4)
    agents.append(a)

r1 = Runner(300, centre, (0, 0), centre)

## Getting coordinates of mouse position
mouse = pygame.mouse.get_pos()

agents[0].target = mouse
agents[0].col = WHITE

screen.fill(BLACK)

## Window runtime loop
win_loop = True
while win_loop:
    ## Refills background
    screen.fill(BLACK)
    
    rand_col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    
    ## Getting coordinates of mouse position
    mouse = pygame.mouse.get_pos()
    
    r1.move()
    r1.draw()
    r1.t += ang_speed
    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False

    for agent in agents:
        agent.fx, agent.fy = 0, 0
        agent.ax, agent.ay = 0, 0
        
        next_x = r1.origin[0] + (r1.path_radius * math.cos(r1.t+(ang_speed*10)))
        next_y = r1.py = r1.origin[1] + (r1.path_radius * math.sin(r1.t+(ang_speed*10)))
        
        agent.target = (next_x, next_y)
        
        
        if distance((agent.px, agent.py), agent.target) <= target_radius:
            agent.arrive()
    
    
        #agent.seekTarget(agent.target)
        agent.seekTarget(agent.target)
        agent.move()
    
        agent.draw()
   
        agent.bounce()
    
    
    
    ## Update screen
    pygame.display.flip()
    clock.tick(60)
    
## Close window
pygame.quit()
sys.exit()