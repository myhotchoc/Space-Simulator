# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 07:51:52 2020

@author: Danny
"""

import pygame
import math
import random

## Hold mouse button to stop gravity
## Press left or right arrow keys to add wind to left or right

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)
YELLOW = (242, 224, 63)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

g = 1
mu = 0.1

vel_limit = 20

windLeftVector = [-75 ,0]
windRightVector = [75, 0]

gravity = False
windRight = False
windLeft = False

## Setting window size, defining screen
win_size = (900, 900)
screen = pygame.display.set_mode(win_size)

## Defining centre of screen
centre = (int(win_size[0]/2), int(win_size[1]/2))

## Initialise window
pygame.init()

## Defining clock object
clock = pygame.time.Clock()

## Window runtime loop
win_loop = True

def magDir(x, y):
    return math.sqrt(x**2 + y**2), atan2(y, x)

def resolve(mag, t):
    return mag*math.cos(t), mag*math.sin(t)

def mag(x, y):
    return math.sqrt(x**2 + y**2)

def setMag(x, y, m):
    
    magnitude = mag(x, y)
    
    if magnitude == 0:
        return 0, 0
    else:
    
        x = x/magnitude * m
        y = y/magnitude * m
    
    return x, y

def unitVector(x, y):
    x, y = setMag(x, y, 1)
    
    return x, y

def limit(x, y, a):
    if mag(x, y) >= a:
        x, y = setMag(x, y, a)
        
    return x, y

def drawArrow(screen, colour, start, end):
    pygame.draw.line(screen,colour,start,end,2)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    pygame.draw.polygon(screen, colour, ((end[0]+20*math.sin(math.radians(rotation)), end[1]+20*math.cos(math.radians(rotation))), (end[0]+20*math.sin(math.radians(rotation-120)), end[1]+20*math.cos(math.radians(rotation-120))), (end[0]+20*math.sin(math.radians(rotation+120)), end[1]+20*math.cos(math.radians(rotation+120)))))

class Body(object):
    def __init__(self, col, mass, p, v, a, f):
        self.col = col
        self.mass = mass
        self.radius = int(math.sqrt(mass) * 3)
        
        self.px = p[0]
        self.py = p[1]
        
        self.vx = v[0]
        self.vy = v[1]
        
        self.ax = a[0]
        self.ay = a[1]
        
        self.fx = f[0]
        self.fy = f[1]
        
        self.weight = [0, self.mass * g]
    
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
        
        drawArrow(screen, (100, 50, 231), (self.px, self.py),(self.px+self.fx, self.py+self.fy))
        
    def friction(self):
        
        unit_vx, unit_vy = unitVector(-self.vx, -self.vy)
        N = self.mass
        
        fric_x = unit_vx * mu * N
        fric_y = unit_vy * mu * N
        
        self.applyForce((fric_x, fric_y))
        
    
#Body(col, mass, radius, p, v, a, f)
body1 = Body(RED, 50, (win_size[0]/4, centre[1] - int((math.sqrt(50) * 3))),
             (0, 0),
             (0, 0),
             (0, 0))

body2 = Body(BLUE, 100, (win_size[0]/2, win_size[1] - int((math.sqrt(100) * 3))),
             (0, 0),
             (0, 0),
             (0, 0))

body3 = Body(GREEN, 200, (3*win_size[0]/4, win_size[1] - int((math.sqrt(200) * 3))),
             (0, 0),
             (0, 0),
             (0, 0))

bodies = [body1, body2, body3]

bodies = [body1]
bodies = []

for x in range(1, 11):
    body = Body((random.randint(0, 255), random.randint(0,255), random.randint(0, 255)),
                25*x,
                (x * win_size[0]/10, centre[1]),
                (random.randint(-10,10), random.randint(-10,10)), 
                (0, 0),
                (0, 0))
    bodies.append(body)




while win_loop:
    ## Refills background
    screen.fill((0, 0, 0))
    

    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False
            
        if i.type == pygame.MOUSEBUTTONDOWN:
            gravity = False
        
        if i.type == pygame.MOUSEBUTTONUP:
            gravity = True
        
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_RIGHT:
                windRight = True
            if i.key == pygame.K_LEFT:
                windLeft = True
        
        if i.type == pygame.KEYUP:
            if i.key == pygame.K_RIGHT:
                windRight = False
            if i.key == pygame.K_LEFT:
                windLeft = False
    
    for i in bodies:
        
        i.ax, i.ay = 0, 0
        i.fx, i.fy = 0, 0
    
        if gravity == True:
            i.applyForce(i.weight)
        
        if windRight == True:
            i.applyForce(windRightVector)
        
        if windLeft == True:
            i.applyForce(windLeftVector)
        
        i.friction()
        
        i.changeAcc()
        #i.ax, i.ay = setMag(i.ax, i.ay, 0.5)
        i.changeVel()
        
        i.vx, i.vy = limit(i.vx, i.vy, vel_limit)
        
        
        if i.px + i.vx + i.radius >= win_size[0] or i.px + i.vx - i.radius <= 0:
            i.vx = -i.vx
            
        if i.py + i.vy + i.radius >= win_size[1] or i.py + i.vy - i.radius <= 0:
            i.vy = -i.vy
        
        i.changePos()
            
        pygame.draw.circle(screen, i.col, (i.px, i.py), i.radius)

    ## Update screen
    pygame.display.flip()
    clock.tick(60)
    
## Close window
pygame.quit()