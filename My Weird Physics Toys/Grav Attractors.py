# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 04:07:13 2020

@author: Danny
"""

import pygame
import math
import random

## Left click to make attracter
## Right click to make repeller
## Press space to make new body

## be careful tho if you have too many thingies on screen it lags a lot
## cos I am bad at making efficient codey things
## complexity is O(n^2) in each frame whoooooo

## Also make a new body (space) before you make attracters
## and repellers idk why it bugs out if you do bodies first you figure it out 

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)
YELLOW = (242, 224, 63)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

vel_limit = 20
f_limit = 100

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

def distance(self, body2):
    ## Difference in x-pos and y-pos
    delta_x = body2.px - self.px
    delta_y = body2.py - self.py
    
    ## Uses Pythagorean Theorem
    return math.sqrt((delta_x)**2 + (delta_y)**2)

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
        
    def changePos(self):
        
        self.px = int(self.px + self.vx)
        self.py = int(self.py + self.vy)
    
    def changeVel(self):
        self.vx += self.ax
        self.vy += self.ay
        
    def changeAcc(self):
        self.ax += self.fx/self.mass
        self.ay += self.fy/self.mass
    
class Attracter(Body):
    def __init__(self, G, p, col):
        self.G = G
        Body.__init__(self, col, 10, p, (0, 0), (0, 0), (0,0))
    
    def attract(self, body):
        
        r = distance(self, body)
        dir_x, dir_y = unitVector((self.px - body.px), (self.py-body.py))
        
        if r != 0:
            strength = self.G * (self.mass * body.mass) / r**2
        else:
            strength = 100
        
        fx, fy = setMag(dir_x, dir_y, strength)
        
        fx, fy = limit(fx, fy, f_limit)
        
        body.fx += fx
        body.fy += fy
        #print (body.fx, body.fy)

#a1 = Attracter(3000, (centre[0], centre[1]))

bodies = []
attracters = []

while win_loop:
    ## Refills background
    screen.fill((0, 0, 0))
    
    mousex = pygame.mouse.get_pos()[0]
    mousey = pygame.mouse.get_pos()[1]
    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False
            
        if i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 1:
                ##left click
                new_attracter = Attracter(300, (mousex, mousey), WHITE)
                attracters.append(new_attracter)
                
            if i.button == 3:
                ##right click
                new_attracter = Attracter(-300, (mousex, mousey), BLUE)
                attracters.append(new_attracter)
        
        if i.type == pygame.KEYDOWN and i.key == pygame.K_SPACE:
            ##space bar
            new_body = Body((random.randint(0,255), random.randint(0, 255), random.randint(0, 255)),
             50, (mousex, mousey),
             (5, 0),
             (0, 0),
             (0, 0))
            
            bodies.append(new_body)


    
    for i in bodies:
        i.fx, i.fy = 0, 0
        for j in attracters:
            
            print (i.fx, i.fy)
            
            j.attract(i)
            
            print (i.fx, i.fy)
            print ()
            
            pygame.draw.circle(screen, j.col, (j.px, j.py), j.radius)
        
        i.ax, i.ay = 0, 0
        #i.fx, i.fy = 0, 0
        
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