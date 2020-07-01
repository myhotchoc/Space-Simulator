# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 10:14:16 2020

@author: Danny
"""

import pygame
import math
import random

## Defining colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)
YELLOW = (242, 224, 63) 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

## I don't know why these are still here
g = 9.81
vel_limit = 30

## Setting window size, defining screen
win_size = (1000, 1000)
screen = pygame.display.set_mode(win_size)

## Defining centre of screen
centre = (int(win_size[0]/2), int(win_size[1]/2))

## Initialise window
pygame.init()

## Defining clock object
clock = pygame.time.Clock()

## Window runtime loop
win_loop = True

## Returns magnitude, direction of a vector
def magDir(x, y):
    return math.sqrt(x**2 + y**2), round(math.atan2(y, x), 5)

## Returns x and y components of a vector
def resolve(mag, t):
    return mag*math.cos(t), mag*math.sin(t)

## Returns direction of a vector
def direction(x, y):
    print (math.atan2(y, x))
    return math.atan2(y, x)

## Returns magnitude of a vector
def mag(x, y):
    return math.sqrt(x**2 + y**2)

## Scales a vector to specified magnitude
def setMag(x, y, m):
    
    magnitude = mag(x, y)
    
    if magnitude == 0:
        return 0, 0
    else:
    
        x = x/magnitude * m
        y = y/magnitude * m
    
    return x, y

## Scale vector to unit length
def unitVector(x, y):
    x, y = setMag(x, y, 1)
    
    return x, y

## Limit magnitude of a vector to given magnitude
def limit(x, y, a):
    if mag(x, y) >= a:
        x, y = setMag(x, y, a)
        
    return x, y

## Body class
## colour, mass, position (x,y), velocity (x,y), acceleration(x,y), force(x,y), 
## amplitude(x,y), theta(x,y), frequency(x,y)
    
class Body(object):
    def __init__(self, col, mass, p, v, a, f, amp, theta, freq):
        self.col = col
        self.mass = mass
        
        self.radius = int(math.sqrt(mass) * 3)
        
        self.px = p[0]
        self.py = p[1]
        
        self.axis = (self.px, self.py)
        
        self.vx = v[0]
        self.vy = v[1]
        
        self.ax = a[0]
        self.ay = a[1]
        
        self.fx = f[0]
        self.fy = f[1]
        
        self.ampx = amp[0]
        self.ampy = amp[1]
        
        self.thetax = theta[0]
        self.thetay = theta[1]
        
        self.freqx = freq[0]
        self.freqy = freq[1]
        
        self.weight = [0, self.mass * g]
    
    ## Update body position
    def changePos(self):
        
        #self.px = int(self.px + self.vx)
        #self.py = int(self.py + self.vy)
        
        ## Defines position to be output of sine function
        ## Amplitude * sin(angle)
        self.px = self.axis[0] + int(self.ampx * math.sin(self.thetax))
        self.py = self.axis[1] + int(self.ampy * math.sin(self.thetay))
        
        ## Increment angle of rotation by frequency
        self.thetax += self.freqx
        self.thetay += self.freqy
        
    ## Makes objects move to mouse but this probably won't work on this program so ignore me
    def moveToMouse(self, mouse):
        self.ax = mouse[0] - self.px
        self.ay = mouse[1] - self.py
        
        self.ax, self.ay = setMag(self.ax, self.ay, acc_val)
        
        self.vx, self.vy = limit(self.vx, self.vy, vel_limit)
    
    ## Makes objects bounce off walls but this also probably doesn't work on this
    def bounce(self):
        if self.px + self.vx >= win_size[0] or self.px + self.vx < 0:
            self.vx = -self.vx
            
        if self.py + self.vy >= win_size[1] or self.py + self.vy < 0:
            self.vy = -self.vy
        
        #self.changePos()
    
    ## Makes objects stick to walls but irrelavent to this program
    def stick(self):
            
        if self.py + self.vy >= win_size[1] - (1 * self.radius) or self.py + self.vy - self.radius <= 0:
            self.py = win_size[1] - (1 * self.radius)
        else:
            self.changePos()
    
    ## Makes line from body to centre of screen cos it looks cool
    def lineToCentre(self):
        
        ## screen, colour, start pos, end pos, width
        pygame.draw.line(screen, WHITE, (self.px, self.py), self.axis, 2)
            

bodiesNum = 50

spacing = (win_size[0])/bodiesNum

bodies = []
for i in range(bodiesNum):
    b = Body((i*(255/bodiesNum), 50, 255),
             20, (i * spacing, centre[1]),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 250),
              (0, 0.2 * i),
              (0, 0.05))
    bodies.append(b)

## Main runtime loop
while win_loop:
    ## Refills background
    screen.fill(BLACK)    
    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False
    
    ## For all bodies in body array
    for i in bodies:
        ## Change position (which does the fancy sine stuff)
        i.changePos()
        ## Draw line to centre
        #i.lineToCentre()
        
        ## Draw circle to screen
        pygame.draw.circle(screen, i.col, (int(i.px), int(i.py)), i.radius)

    ## Update screen
    pygame.display.flip()
    clock.tick(60)
    
## Close window
pygame.quit()