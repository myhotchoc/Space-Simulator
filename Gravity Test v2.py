# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 19:50:43 2020

@author: Danny
"""

import pygame
import random
import math

## Gravitational constant but I changed the value because this is not my universe and I am not god
G = 10 

## Resolves vector into x and y components, returns (x, y) for <magnitude, angle>
def resolve(mag, t):
    return (mag * math.cos(t), mag * math.sin(t))

## Class for body
class Body(object):
    
    ## mass, initial speed (magDir-tuple), position (xy-tuple), colour (rgb-tuple)
    def __init__(self, mass, u, pos, colour):
        self.mass = mass
        self.pos = pos
        self.colour = colour
        
        ## Sets x and y components of initial and final velocities
        self.u_x = resolve(u[0], u[1])[0]
        self.u_y = resolve(u[0], u[1])[1]
        
    
    ## Returns distance between body and second body b2
    def distance(self, b2):
        ## Pythagorean Theorem for distance
        return math.sqrt((self.pos[0] - b2.pos[0])**2 + (self.pos[1] - b2.pos[1])**2)
    
    ## Returns force between body and second body b2
    def force(self, b2):
        ## Calculate distance
        d = self.distance(b2)
        
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
    def acceleration(self, f):
        
        ## F=ma
        return (f[0]/self.mass, f[1]/self.mass)

    ## returns tuple of change in x, change in y
    def displacement(self, a):
        
        ## v = u+at (t=1)
        self.v_x = self.u_x + a[0]
        self.v_y = self.u_y + a[1]
        
        ## v^2 - u^2 = 2as
        
        ## If statements to prevent division by 0 and Python throwing a hissy fit at me
        if a[0] == 0:
            s_x = 0
        else:
            s_x = ((self.v_x ** 2) - (self.u_x ** 2))/ (2 * a[0])
        
        
        if a[1] == 0:
            s_y = 0
        else:
            s_y = ((self.v_y ** 2) - (self.u_y ** 2))/ (2 * a[1])
        
        ## Updating initial velocity for next iteration
        self.u_x= self.v_x
        self.u_y = self.v_y
        
        ## Returns new position=old position + displacement
        return (s_x + self.pos[0], s_y + self.pos[1])

    ## Change position of body
    def changePos(self, s):
        self.pos = (int(s[0]), int(s[1]))
        
## Setting window size, defining screen
win_size = (750, 750)
screen = pygame.display.set_mode(win_size)

## Defining centre of screen
centre = (int(win_size[0]/2), int(win_size[1]/2))

## Initialise window
pygame.init()

## Defining clock object
clock = pygame.time.Clock()

## Body(mass, u(mag,dir), pos(x,y), col(rgb))
## Defining 2 bodies
body1 = Body(100, (10, math.pi/2), (int(win_size[1]/4), int(win_size[1]/2)), (255,0,0))
body2 = Body(100, (0, 0), (int(3*win_size[1]/4), int(win_size[1]/2)), (0,0,255))

## Window runtime loop
win_loop = True
while win_loop:
    
    ## Refills background
    screen.fill((255, 255, 255))
    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False
    
    ## Placing two bodies on screen
    pygame.draw.circle(screen, body1.colour, body1.pos, 20)
    pygame.draw.circle(screen, body2.colour, body2.pos, 20)
    
    ## Calculates force between bodies due to gravity
    f = body1.force(body2)
    
    ## Calculates each body's acceleration
    a1 = body1.acceleration(f)
    a2 = body2.acceleration(f)
    
    ## Calculates each body's new position
    s1 = body1.displacement(a1)
    s2 = body2.displacement(a2)
    
    ## Changes position of each body
    body1.changePos(s1)
    body2.changePos(s2)
    
    ## Update screen
    pygame.display.flip()
    clock.tick(60)


## Close window
pygame.quit()