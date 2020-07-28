# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 02:49:27 2020

@author: Danny
"""

import pygame, sys, math, random

## Colours
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
ORANGE = [255, 128, 0]
YELLOW = [242, 224, 63]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
LIGHT_BLUE = [0,  255, 255]
PINK = [255, 153, 255]
LIME = [128, 255, 0]

rand_col = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

## Setting window size, defining screen
win_size = (900, 900)
screen = pygame.display.set_mode(win_size)

## Defining centre of screen
centre = [int(win_size[0]/2), int(win_size[1]/2)]

## Initialise window
pygame.init()

## Defining clock object
clock = pygame.time.Clock()

def distance(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    
    return ((dx**2) + (dy**2))**0.5


tri = [
       [centre[0]+100, centre[1]],
       [centre[0]+50, centre[1]-50],
       centre
       ]


theta = 0.1



def rotate(origin, point, angle):

    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) + math.sin(angle) * (py - oy)
    qy = oy - math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

xtot = 0
ytot = 0
for i in tri:
    xtot += i[0]
    ytot += i[1]
    
centroid = (xtot/3, ytot/3)
print (centroid)

## Window runtime loop
win_loop = True
while win_loop:
    ## Refills background
    screen.fill((255, 255, 255))
    
    ## Getting coordinates of mouse position
    mouse = pygame.mouse.get_pos()
    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False

    
    pygame.draw.polygon(screen, BLUE,
                        tri,
                        10)
    
    
    for i in tri:
        print (i)
        i[0], i[1] = rotate(centroid, i, theta)
    
    print (tri)
    
    #tri = rotatePoints(tri, theta)
    #theta += 0.001
    
    ## Update screen
    pygame.display.flip()
    clock.tick(60)
    
## Close window
pygame.quit()
sys.exit()