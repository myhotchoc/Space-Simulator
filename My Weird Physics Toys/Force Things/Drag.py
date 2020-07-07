# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 07:46:23 2020

@author: Danny
"""

## Different drag/fluid resistances in different 'liquids'
## Change c1, c2, c3 for resistances in air, water, oil

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
LIGHTBLUE = (76, 181, 204)

g = 9.8
vel_limit = 30

c1 = 10
c2 = 100
c3 = 500


## Setting window size, defining screen
win_size = (900, 900)
screen = pygame.display.set_mode(win_size)

## Defining centre of screen
centre = (int(win_size[0]/2), int(win_size[1]/2))

blue_y = centre[1]
yellow_y = centre[1] + 250

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

def drawArrow(screen, colour, start, end):
    pygame.draw.line(screen,colour,start,end,2)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    pygame.draw.polygon(screen, colour, ((end[0]+10*math.sin(math.radians(rotation)), end[1]+10*math.cos(math.radians(rotation))), (end[0]+10*math.sin(math.radians(rotation-120)), end[1]+10*math.cos(math.radians(rotation-120))), (end[0]+10*math.sin(math.radians(rotation+120)), end[1]+10*math.cos(math.radians(rotation+120)))))

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
        
        print ('f: ', self.fy)
        
    def applyForce(self, force):
        self.fx += force[0]
        self.fy += force[1]
        #print (self.fy)
        
        drawArrow(screen, (100, 255, 0), (self.px, self.py),(self.px +force[0] , self.py+force[1]*0.1 ))
        
    
    def drag(self):
        
        if self.py >= yellow_y:
            c = c3
        elif self.py >= blue_y:
            c = c2
        else:
            c = c1
        
        
        unit_vx, unit_vy = unitVector(-self.vx, -self.vy)
        N = self.mass
        
        m = c * (mag(i.vx, i.vy) ** 2)
        
        di = direction(unit_vx, unit_vy)
        
        drag_x, drag_y = resolve(m, di)
        
        
        #drag_x = unit_vx * c * (i.vx**2)
        #drag_y = unit_vy * c * (i.vy**2)
        #drawArrow(screen, (100, 255, 0), (self.px, self.py),(self.px +self.fx , self.py+self.fy * 0.5))
        
        #print ('d: ', drag_y)
        self.applyForce((round(drag_x, 5), round(drag_y, 5)))
        
body1 = Body(RED, 100, (win_size[0]/3, 100),
             (0, 0),
             (0, 0),
             (0, 0))

body2 = Body(BLUE, 200, (2 * win_size[0]/3, 100),
             (0, 0),
             (0, 0),
             (0, 0))

bodies = [body1, body2]
        
while win_loop:
    ## Refills background
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, LIGHTBLUE, (0, blue_y, win_size[0], win_size[1]))
    pygame.draw.rect(screen, YELLOW, (0, yellow_y, win_size[0], win_size[1]))
    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False
    
    for i in bodies:
        
        #i.ax, i.ay = 0, 0
        i.fx, i.fy = 0, 0
        
        i.applyForce(i.weight)
        i.drag()
        
        i.changeAcc()
        i.ax, i.ay = setMag(i.ax, i.ay, 0.5)
        i.changeVel()
        
        i.vx, i.vy = limit(i.vx, i.vy, vel_limit)
        
        
        if i.px + i.vx + i.radius >= win_size[0] or i.px + i.vx - i.radius <= 0:
            i.vx = -i.vx
            
        if i.py + i.vy >= win_size[1] - (1 * i.radius) or i.py + i.vy - i.radius <= 0:
            #i.vy = -i.vy
            i.py = win_size[1] - (1 * i.radius)
            #i.py = 0
            #pass
        else:
            i.changePos()
            
        pygame.draw.circle(screen, i.col, (i.px, i.py), i.radius)

    ## Update screen
    pygame.display.flip()
    clock.tick(60)
    
## Close window
pygame.quit()