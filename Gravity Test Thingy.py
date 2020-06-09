# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 07:24:27 2020

@author: Danny
"""
## Please don't try and read this yet it is a big mess of sphagetti
## Now im hungry and I want spahgetti
## Better idea im having pasta
## P.s. u smell

import pygame
import random
import math

win_size = (750, 750)
screen = pygame.display.set_mode(win_size)

# Defining centre of screen
centre = (int(win_size[0]/2), int(win_size[1]/2))

#Initialise window
pygame.init()

clock = pygame.time.Clock()

c1_pos = [int(2 * centre[0]/3), centre[1]]
c2_pos = [int(4 * centre[0]/3), centre[1]]

#c1_mass = 5.972*10**24
#c2_mass = 7.35*10**22

c1_mass = 30
c2_mass = 20

c1_u = (10*math.cos(math.pi/4), 20*math.sin(math.pi/6))
c2_u = (20*math.cos(math.pi/4), 40*math.sin(math.pi/4))

c1_v = (0, 0)
c2_v = (0, 0)



def changePos():
    distance = math.sqrt((c1_pos[0] - c2_pos[0])**2 + (c1_pos[1] - c2_pos[1])**2)
    
    #force = (((6.674 * (10**-11)) * c1_mass * c2_mass) / distance) / 10**11
    force = (((500 * c1_mass * c2_mass) / distance))
    
    c1_a = force/c1_mass
    c2_a = force/c2_mass
    
    print (((((c1_v[0]) ** 2) - ((c1_u[0]) ** 2))/(2 * c1_a), (((c1_v[1]) ** 2) - ((c1_u[1]) ** 2))/(2 * c1_a)))
    s = ((((c1_v[0]) ** 2) - ((c1_u[0]) ** 2))/(2 * c1_a), (((c1_v[1]) ** 2) - ((c1_u[1]) ** 2))/(2 * c1_a))
    
    
    c1_s = ((((c1_v[0]) ** 2) - ((c1_u[0]) ** 2))/(2 * c1_a), (((c1_v[1]) ** 2) - ((c1_u[1]) ** 2))/(2 * c1_a))
    c2_s = ((((c2_v[0]) ** 2) - ((c2_u[0]) ** 2))/(2 * c2_a), (((c2_v[1]) ** 2) - ((c2_u[1]) ** 2))/(2 * c2_a))

    print ('f: ', force)
    
    print (c1_s, c2_s)
    
    if c1_s[1] > 5:
        c1_s = 2
    if c2_s[1] > 5:
        c2_s=2
    
    c1_pos[0] += int(c1_s[0])
    c1_pos[1] += int(c1_s[1])
    c2_pos[0] += int(c2_s[0])
    c2_pos[1] += int(c2_s[1])

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