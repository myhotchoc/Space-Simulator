# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 07:50:32 2020

@author: Danny
"""

import pygame
import math
import random


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
    def __init__(self, col, mass, p, v, a, f, angle, angVel, angAcc):
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
        
        self.angle = angle
        self.angVel = angVel
        self.angAcc = angAcc
    
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
        
# =============================================================================
#     def rotate(self, theta):
#         self.px = (self.px * math.cos(theta)) - (self.py * math.sin(theta))
#         self.py = (self.px * math.sin(theta)) + (self.py * math.cos(theta))
# =============================================================================
        
    def rotate(self,angle):
        pygame.transform.rotate(self, angle)
    
    def changeAng(self):
        self.angle += self.angVel
    
    def changeAngVel(self):
        self.angVel += self.angAcc
    
        
        #drawArrow(screen, (100, 255, 0), (self.px, self.py),(self.px +force[0] , self.py+force[1]*0.1 ))
        
body1 = Body(GREEN, 100, (centre[0], centre[1]),
             (0, 0),
             (0, 0),
             (0, 0),
             math.pi/2, 0, 0)

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
        
        #i.applyForce(i.weight)
        
        i.changeAcc()
        i.ax, i.ay = setMag(i.ax, i.ay, 0.5)
        i.changeVel()
        
        i.vx, i.vy = limit(i.vx, i.vy, vel_limit)
        i.angAcc = 0.01
        
        i.changeAngVel()
        #i.changeAng()
        
        
        i.rotate(i.angVel)
        
        if i.px > win_size[0] or i.px < 0 or i.py > win_size[1] or i.py < 0:
            i.px, i.py = centre[0], centre[1]
        
        if i.px + i.vx + i.radius >= win_size[0] or i.px + i.vx - i.radius <= 0:
            i.vx = -i.vx
            
        if i.py + i.vy >= win_size[1] - (1 * i.radius) or i.py + i.vy - i.radius <= 0:
            #i.vy = -i.vy
            i.py = win_size[1] - (1 * i.radius)
            #i.py = 0
            #pass
        else:
            i.changePos()
            
        pygame.draw.rect(screen, i.col, (i.px - 100, i.py - 100, 200, 200))

    ## Update screen
    pygame.display.flip()
    clock.tick(60)
    
## Close window
pygame.quit()