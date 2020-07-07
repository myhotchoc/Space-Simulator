# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 02:49:27 2020

@author: Danny
"""

import pygame, sys, math

# Defining Colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)
YELLOW = (242, 224, 63) 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
rand_col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

g = 9.81

class Pendulum(object):
    def __init__(self, size, colour, origin, theta, length, angVel, angAcc, damping):
        self.size = size
        self.colour = colour
        
        self.originx = origin[0]
        self.originy = origin[1]
        
        self.theta = theta
        self.length = length
        
        self.angVel = angVel
        self.angAcc = angAcc
        
        self.grav_force = 0.01
        self.damping = damping
    
    def changePos(self):
        self.x = int(self.length * math.sin(self.theta)) + self.originx
        self.y = -int(self.length * math.cos(self.theta)) + self.originy

    
    def drawBody(self):
        pygame.draw.line(screen, self.colour, (self.originx, self.originy),
                         (self.x, self.y), 2)
        
        pygame.draw.circle(screen, WHITE, (self.originx, self.originy), 15)
    
    def changeAng(self):
        self.theta += self.angVel
    
    def changeAngVel(self):
        self.angVel += self.angAcc
    
    def drawBob(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size)

## Setting window size, defining screen
win_size = (900, 900)
screen = pygame.display.set_mode(win_size)

## Defining centre of screen
centre = (int(win_size[0]/2), int(win_size[1]/2))

## Initialise window
pygame.init()

## Defining clock object
clock = pygame.time.Clock()

pendulums = []
pendNums = 40

for i in range(1, pendNums+1):
    p = Pendulum(20, (150, i*(255/(pendNums)), i*(255/(pendNums))),
                 (centre[0], 200),
                 math.pi/2, 100 + i*15,
                 0, 0, 0.995)
    pendulums.append(p)


## Window runtime loop
win_loop = True
while win_loop:
    ## Refills background
    screen.fill(BLACK)
    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False
    
    
    
    for p in pendulums:
        p.changePos()
        
        p.changeAngVel()
        p.changeAng()
        
        p.drawBob()
        p.drawBody()
        
        p.angAcc = p.grav_force * math.sin(p.theta) / p.length * 100
        p.angVel = (p.angVel * p.damping)
        
        #print (p.angVel, p.theta)
    
    ## Update screen
    pygame.display.flip()
    clock.tick(60)
    
## Close window
pygame.quit()
sys.exit()