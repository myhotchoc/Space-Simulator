# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 07:50:32 2020

@author: Danny
"""

import pygame
import math
import random

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)
YELLOW = (242, 224, 63) 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

g = 9.81
vel_limit = 30

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
    return math.sqrt(x**2 + y**2), round(math.atan2(y, x), 5)

def resolve(mag, t):
    return mag*math.cos(t), mag*math.sin(t)

def direction(x, y):
    print (math.atan2(y, x))
    return math.atan2(y, x)

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


def changePos(px, py, vx, vy):
    
    px += vx
    py += vy
    
    return px, py

def changeVel(vx, vy, ax, ay):
    vx += ax
    vy += ay
    
    return vx, vy
    
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
        #print (self.fy)
        
        #drawArrow(screen, (100, 255, 0), (self.px, self.py),(self.px +force[0] , self.py+force[1]*0.1 ))
    
    def moveToMouse(self, mouse):
        self.ax = mouse[0] - self.px
        self.ay = mouse[1] - self.py
        
        self.ax, self.ay = setMag(self.ax, self.ay, acc_val)
        
        self.changeVel()
        
        self.vx, self.vy = limit(self.vx, self.vy, vel_limit)
        self.changePos()
    
    def bounce(self):
        if self.px + self.vx >= win_size[0] or self.px + self.vx < 0:
            self.vx = -self.vx
            
        if self.py + self.vy >= win_size[1] or self.py + self.vy < 0:
            self.vy = -self.vy
        
        self.changePos()
    
    def stick(self):
            
        if self.py + self.vy >= win_size[1] - (1 * self.radius) or self.py + self.vy - self.radius <= 0:
            #i.vy = -i.vy
            self.py = win_size[1] - (1 * self.radius)
            #i.py = 0
            #pass
        else:
            self.changePos()
            
        
body1 = Body(RED, 100, (win_size[0]/2, 100),
             (0, 0),
             (0, 0),
             (0, 0))

bodies = [body1]

while win_loop:
    ## Refills background
    screen.fill((0, 0, 0))
    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False
    
    for i in bodies:
        
        #i.ax, i.ay = 0, 0
        i.fx, i.fy = 0, 0
        
        i.applyForce(i.weight)
        
        i.changeAcc()
        i.ax, i.ay = setMag(i.ax, i.ay, 0.5)
        
        i.changeVel()
        
        i.vx, i.vy = limit(i.vx, i.vy, vel_limit)
        
        #i.bounce()
        i.stick()
        
        i.changePos()
            
        pygame.draw.circle(screen, i.col, (i.px, i.py), i.radius)

    ## Update screen
    pygame.display.flip()
    clock.tick(60)
    
## Close window
pygame.quit()