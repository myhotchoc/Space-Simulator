# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 07:24:27 2020

@author: Danny
"""

import pygame
import random

win_size = (750, 750)
screen = pygame.display.set_mode(win_size)

# Defining centre of screen
centre = (int(win_size[0]/2), int(win_size[1]/2))

#Initialise window
pygame.init()

clock = pygame.time.Clock()

c1_pos = [int(2 * centre[0]/3), centre[1]]
c2_pos = [int(4 * centre[0]/3), centre[1]]

c1_mass = 5.972*10**24
c2_mass = 7.35*10**22

c1_u = 5
c2_u = 5

c1_v = 0
c2_v = 0

print (centre)
print (c1_pos, c2_pos)

def changePos():
    distance = math.sqrt((c1_pos[0] - c2_pos[0])**2 + (c1_pos[1] - c2_pos[1])**2)
    
    force = (((6.674 * (10**-11)) * c1_mass * c2_mass) / distance) / 10**11
    
    c1_a = force/c1_mass
    c2_a = force/c2_mass
    
    c1_s = (((c1_v) ** 2) - ((c1_u) ** 2))/(2 * c1_a)
    c2_s = (((c2_v) ** 2) - ((c2_u) ** 2))/(2 * c2_a)
    
    print ('f: ', force)
    
    print (c1_s, c2_s)
    
    if c1_s > 500:
        c1_s = 100
    if c2_s > 500:
        c2_s=100
    
    c1_pos[0] += int(c1_s)
    c2_pos[0] += int(c2_s)

win_loop = True
while win_loop:
    screen.fill((255, 255, 255))
    
    c1 = pygame.draw.circle(screen, (255, 0, 0), c1_pos, 20)
    c2 = pygame.draw.circle(screen, (0, 0, 255), c2_pos, 20)
    changePos()
    
    
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()