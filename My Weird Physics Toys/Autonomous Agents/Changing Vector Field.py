# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 02:49:27 2020

@author: Danny
"""

import pygame, sys, math, random, copy
from perlin import *

## Colours
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
ORANGE = [255, 128, 0]
YELLOW = [242, 224, 63]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
LIGHT_BLUE = [3, 227, 252]
PINK = [255, 153, 255]
LIME = [128, 255, 0]
PURPLE = [107, 3, 252]

rand_col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
colours = [RED, ORANGE, YELLOW]


## Setting window size, defining screen
win_size = (900, 900)
screen = pygame.display.set_mode(win_size)

## Defining centre of screen
centre = (int(win_size[0]/2), int(win_size[1]/2))

## Initialise window
pygame.init()

## Defining clock object
clock = pygame.time.Clock()

## Subtract two vectors:
def subtract(a, b):
    
    new_vec = []
    for i in range(len(a)):
        new_vec.append(a[i] - b[i])
    
    return new_vec

## Add two vectors:
def add(a, b):
    
    new_vec = []
    for i in range(len(a)):
        new_vec.append(a[i] + b[i])
    
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

agent_width = 4
agent_height = 8
target_radius = 100
min_speed = 3
max_speed = 6

t = 0

resolution = 100
multiplier = resolution
perlinSize = 10
ang_mult = 0.5
vector_movement = 0.01

randFieldForward = False
perlinField = True
drawVectors = True
background = True

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
        self.t = 0

        
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
        self.fx = self.fx + force[0]
        self.fy = self.fy + force[1]
        
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
        
    ## Calculates steering force of agent
    def seekTarget(self):

        ## Find desired direction
        temp = copy.deepcopy(flow_field.getVector(self))
        self.desired = temp
        #self.desired = [0, 4]

        ## Magnitude of desired direction vector
        dist =  mag(agent.desired[0], agent.desired[1])
        agent.desired[0], agent.desired[1] = setMag(agent.desired[0], agent.desired[1], agent.max_speed)
        
        ## Find steer vector (steer = desired-velocity)
        self.steer = subtract(self.desired, (self.vx, self.vy))
        ## Limit steer vector to maximum force
        self.steer[0], self.steer[1] = limit(self.steer[0], self.steer[1], self.max_force)
        
        
        ## Apply steer as a force
        self.applyForce(self.steer)
    
    ## Arrival method
    def arrive(self, distance):
        
        ## Map new speed to distance to target
        new_mag = changeRange(0, target_radius, 0, self.max_speed, distance)
        self.vx, self.vy = setMag(self.vx, self.vy, new_mag)
        
    def throughEdges(self):
        if self.px + self.vx >= win_size[0]:
           # self.vx = -self.vx
            self.px = 0
        
        if self.px + self.vx < 0:
          #  self.vx = -self.vx
            self.px = win_size[0]
            
        if self.py + self.vy >= win_size[1]:
           # self.vx = -self.vx
            self.py = 0
            
        if self.py + self.vy < 0:
          #  self.vy = -self.vy
            self.py = win_size[1]
    
        
class FlowField(object):
    def __init__(self, res):
        self.cols = int(win_size[0]/res)
        self.rows = int(win_size[1]/res)
        
        self.res = res
        self.field = []
        
    def genField(self):
    
        if randFieldForward:
            for r in range(self.cols+1):
                self.field.append([])
                for c in range(self.rows+1):
                    
                    rand_vect = [random.uniform(0,2), random.uniform(-1,1)]
                    rand_vect[0], rand_vect[1] = setMag(rand_vect[0], rand_vect[1], multiplier)
    
                    
                    self.field[r].append(rand_vect)
                    #self.field[r].append([2, 1])
                   # print (self.field[r][c])
            
        if perlinField:
            self.field = []
            for r in range(self.cols+1):
                self.field.append([])
                for c in range(self.rows+1):

                    ang = pnf(r/res, c/res, t/frameres)
                    ang = changeRange(-0.1, 0.1, -ang_mult*math.pi, ang_mult*math.pi, ang)
                    x, y = resolve(multiplier, ang)
                    self.field[r].append([x, y])
                    
    
            
    def getVector(self, agent):
        col = int(agent.px/self.res)
        row = int(agent.py/self.res)
    
        vector = self.field[col][row]
        return vector
    
    def drawField(self):
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                
                start_x = i*self.res + (0.5*self.res)
                start_y = j*self.res + (0.5*self.res)
                
                end_x = (i*self.res)+(self.field[i][j][0] )+(0.5*self.res)
                end_y = (j*self.res)+(self.field[i][j][1] )+(0.5*self.res)
                
                pygame.draw.line(screen, YELLOW,
                                 (start_x, start_y),
                                 (end_x, end_y), 2)
    def drawSqaures(self):
        for i in range(len(self.field)-1):
            for j in range(len(self.field[i])-1):
                
                top_left = (i*self.res, j*self.res)
                
                top_right = ((i+1)*self.res, (j)*self.res)
                
                bottom_right = (
                        ((i+1)*self.res),
                        ((j+1)*self.res)
                               )
                    
                bottom_left = (i*self.res,
                               ((j+1)*self.res)
                               )
                
                pygame.draw.polygon(screen, (50, 50, 50),
                                    (top_left, top_right, bottom_right, bottom_left),
                                    1)
                

flow_field = FlowField(resolution)
flow_field.genField()
flow_field.drawField()

#print (ff.field)
agents = []


def makeAgent(pos):
    a = a = Agent(random.choice(colours),
                  pos,
              (0, 0), (0, 0), (0, 0), random.uniform(min_speed,max_speed), 0.3)
    agents.append(a)




for i in range(1):
    a = Agent(WHITE, (random.randint(100, 800), random.randint(100, 800)),
              (0, 0), (0, 0), (0, 0), 8, 0.4)
    agents.append(a)


## Getting coordinates of mouse position
mouse = pygame.mouse.get_pos()

agents[0].target = mouse
agents[0].col = WHITE

screen.fill(BLACK)

button_down = False


## Window runtime loop
win_loop = True
while win_loop:
    if background:
    ## Refills background
        screen.fill(BLACK)
    
    flow_field.genField()
    t += vector_movement
    
    if drawVectors:
        flow_field.drawSqaures()
        flow_field.drawField()
    
    rand_col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    
    ## Getting coordinates of mouse position
    mouse = pygame.mouse.get_pos()
    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False
        
        if i.type == pygame.MOUSEBUTTONDOWN:
            button_down = True
            
        
        if i.type == pygame.MOUSEBUTTONUP:
            button_down = False

   # for i in range(1, len(agents)):
  #      rand_col = random.choice(colours)
    
    if button_down == True:
        makeAgent(mouse)

    for agent in agents:
        #print (agent.offset)
        agent.fx, agent.fy = 0, 0
        agent.ax, agent.ay = 0, 0
        
        
        
        agent.seekTarget()
        
        #agent.bounce()
        agent.throughEdges()
        
        agent.move()
    
        agent.draw()
   
    #print (flow_field.field)
    
    ## Update screen
    pygame.display.flip()
    clock.tick(60)
    
## Close window
pygame.quit()
sys.exit()