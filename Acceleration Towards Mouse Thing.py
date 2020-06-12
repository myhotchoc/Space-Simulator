# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 07:51:52 2020

@author: Danny
"""

import pygame
import math


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
    x = x/magnitude * m
    y = y/magnitude * m
    
    return x, y

def limit(x, y, a):
    if mag(x, y) >= a:
        x, y = setMag(x, y, a)
        
    return x, y

px = centre[0]
py = centre[1]

vx = 4
vy = 4

acc_val = 0.5
vel_limit = 15

def changePos(px, py, vx, vy):
    
    px += vx
    py += vy
    
    return px, py

def changeVel(vx, vy, ax, ay):
    vx += ax
    vy += ay
    
    return vx, vy
    


while win_loop:
    ## Refills background
    screen.fill((0, 0, 0))
    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False
        
    
    mouse = pygame.mouse.get_pos()
    
    accx = mouse[0] - px
    accy = mouse[1] - py
    
    accx, accy = setMag(accx, accy, acc_val)
    
    vx, vy = changeVel(vx, vy, accx, accy)
    
    print (limit(vx, vy, vel_limit))
    
    vx, vy = limit(vx, vy, vel_limit)
    
    
    if px+vx >= win_size[0] or px+vx < 0:
        vx = -vx
        
    if py+vy >= win_size[1] or py+vy < 0:
        vy = -vy
    
    px, py = changePos(px, py, vx, vy)
    
    if px >= win_size[0] or px < 0 or py >= win_size[1] or py <= 0:
        px, py = px, py
        
    pygame.draw.circle(screen, (255, 100, 0), (int(px), int(py)), 20)

    
    ## Update screen
    pygame.display.flip()
    clock.tick(60)
    
## Close window
pygame.quit()