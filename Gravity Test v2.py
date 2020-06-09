# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 19:50:43 2020

@author: Danny
"""

import pygame
import random
import math

## Gravitational constant but I changed the value because this is my universe and I am god
G = 100 

## Resolves vector into x and y components, returns (x, y) for <magnitude, angle>
def resolve(mag, t):
    return (mag * math.cos(t), mag * math.sin(t))

## Class for body
class Body(object):
    
    ## mass, initial speed (magDir-tuple), final speed (magDir-tuple), position (xy-tuple), colour (rgb-tuple)
    def __init__(self, mass, u, v, pos, colour):
        self.mass = mass
        self.pos = pos
        self.colour = colour
        
        ## Sets x and y components of initial and final velocities
        self.u_x = resolve(u[0], u[1])[0]
        self.u_y = resolve(u[0], u[1])[1]
        
        self.v_x = resolve(v[0], v[1])[0]
        self.v_y = resolve(v[0], v[1])[1]
    
    ## Returns distance between body and second body b2
    def distance(b2):
        ## Pythagorean Theorem for distance
        return math.sqrt((self.pos[0] - b2.pos[0])**2 + (self.pos[1] - b2.pos[1])**2)
    
    ## Returns force between body and second body b2
    def force(b2):
        ## Calculate distance
        d = distance(b2)
        
        ## Newton's Law: F=G*m1*m2/d^2
        f = (((G * self.mass * b2.mass) / d**2))
        
        ## Finds difference in x and y components of distance
        y = self.pos[1] - b2.pos[1]
        x = self.pos[0] - b2.pos[0]
        
        ## Finds angle to horizontal between bodies
        theta = math.atan(y/x)
        
        ## Returns x and y components of force
        return resolve(f, theta)
    
    ## Returns acceleration due to force f
    def acceleration(f):
        
        ## F=ma
        return (f[0]/self.mass, f[1]/self.mass)

    def displacement(a):
        s_x = 
        
## Setting window size, defining screen
win_size = (750, 750)
screen = pygame.display.set_mode(win_size)

## Defining centre of screen
centre = (int(win_size[0]/2), int(win_size[1]/2))

## Initialise window
pygame.init()

## Defining clock object
clock = pygame.time.Clock()



## Window runtime loop
win_loop = True
while win_loop:
    
    ## Refills background
    screen.fill((255, 255, 255))
    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False
            
    
    
    
    ## Update screen
    pygame.display.flip()
    clock.tick(60)


## Close window
pygame.quit()