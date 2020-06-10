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
pi = 3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631558817488152092096282925409171536436789259036001133053054882046652138414695194151160943305727036575959195309218611738193261179310511854807446237996274956735188575272489122793818301194912983367336244065664308602139494639522473719070217986094370277053921717629317675238467481846766940513200056812714526356082778577134275778960917363717872146844090122495343014654958537

## Resolves vector into x and y components, returns (x, y) for <magnitude, angle>
def resolve(mag, t):
    if t == pi:
        return (-mag, 0)
    
    if t > pi/2 and t < pi:
        return (mag * math.cos(pi-t), mag * math.sin(pi-t))
    
    elif t > pi and t < 3 * pi/2:
        return (mag * math.cos(pi+t), mag * -math.sin(pi+t))
    
    elif t > 3*pi/2 and t < 2 * pi:
        return (mag * math.cos(t), -mag * math.sin(t))
    
    else:
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
        
        print ('f', f)
        
        ## Finds difference in x and y components of distance
        y = self.pos[1] - b2.pos[1]
        x = self.pos[0] - b2.pos[0]
        
        print ('x, y:', x, y)
        
        ## Finds angle to horizontal between bodies
        
        if x == 0:
            theta = pi/2
        else:
            theta = math.atan(y/x)
        
        print ('theta: ',theta)
        
        ## Returns x and y components of force
        print ('resolved: ', resolve(f, theta))
        print ()
        return resolve(f, theta)
    
    ## Returns acceleration due to force f
    def acceleration(self, f):
        
        ## F=ma
        
        if self.mass != 0:
            return (f[0]/self.mass, f[1]/self.mass)
        else:
            return (0, 0)

    ## returns tuple of change in x, change in y
    def displacement(self, a):
        
        print ('u_x: ', self.u_x)
        print ('a[0]', a[0])
        print ('u_y: ', self.u_y)
        print ('a[1]', a[1])
        
        ## v = u+at (t=1)
        self.v_x = self.u_x + a[0]
        self.v_y = self.u_y + a[1]
        
        print ('\nnew v: ', self.v_x, self.v_y)
        
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
        
        print ('\ndelta s: ', s_x, s_y)
        
        ## Updating initial velocity for next iteration
        self.u_x = self.v_x
        self.u_y = self.v_y
        
        ## Returns new position=old position + displacement
        return (s_x + self.pos[0], s_y + self.pos[1])

    ## Change position of body
    def changePos(self, s):
        self.pos = (int(s[0]), int(s[1]))
        
## Setting window size, defining screen
win_size = (900, 900)
screen = pygame.display.set_mode(win_size)

## Defining centre of screen
centre = (int(win_size[0]/2), int(win_size[1]/2))

## Initialise window
pygame.init()

## Defining clock object
clock = pygame.time.Clock()

## Body(mass, u(mag,dir), pos(x,y), col(rgb))
## Defining 2 bodies
body1 = Body(50, (5, 1), (int(5*win_size[1]/6), int(win_size[1]/2.7)), (255,0,0))
body2 = Body(200, (0,0), (int(win_size[1]/2), int(win_size[1]/2)), (0,0,255))

count = 0

## Window runtime loop
win_loop = True
while win_loop:
    if count >= 4:
        win_loop = False
    ## Refills background
    screen.fill((255, 255, 255))
    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False
    
    ## Placing two bodies on screen
    
    for item in (body1, body2):
        if item.pos[0] >= win_size[0] or item.pos[0] <= 0:
            item.u_x = -item.u_x
        
        if item.pos[1] >= win_size[1] or item.pos[1] <= 0:
            item.u_y = -item.u_y
    
    pygame.draw.circle(screen, body1.colour, body1.pos, 20)
    pygame.draw.circle(screen, body2.colour, body2.pos, 20)
    
    print  ('Init u: ', (body1.u_x, body1.u_y))
    print ('\nInit pos: ', body1.pos, body2.pos)
    
    ## Calculates force between bodies due to gravity
    f = body1.force(body2)
    
    print ('\nForce: ', f)
    
    ## Calculates each body's acceleration
    a1 = body1.acceleration(f)
    #a2 = body2.acceleration(f)
    
    print ('\nAcceleration: ', a1, a2)
    
    ## Calculates each body's new position
    s1 = body1.displacement(a1)
    #s2 = body2.displacement(a2)
    
    print ('\nDisplacement: ', s1, s2)
    print ()
    
    ## Changes position of each body
    body1.changePos(s1)
    #body2.changePos(s2)
    
    ## Update screen
    pygame.display.flip()
    clock.tick(60)

    #count+=1
## Close window
pygame.quit()