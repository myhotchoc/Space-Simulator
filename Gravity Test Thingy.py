# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 07:24:27 2020

@author: Danny and Jenni
"""
## Please don't try and read this yet it is a big mess of sphagetti
## Now im hungry and I want spahgetti
## Better idea im having pasta
## P.s. u smell

##its not a mess, pretty good at understanding i am
##i dont like pasta tbh
##p.p.s you smell worse

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


def resolve(mag, t):
    return (mag * math.cos(t), mag * math.sin(t))

def changePos():
    #pythagorous to find shortest distance
    distance = math.sqrt((c1_pos[0] - c2_pos[0])**2 + (c1_pos[1] - c2_pos[1])**2)
    
    #force = (((6.674 * (10**-11)) * c1_mass * c2_mass) / distance) / 10**11
    
    ## I FORGOT TO SQUARE THE GODDAMN DISTANCE ITS AN INVERSE SQAURE LAW THATS THE WHOLE DAMN POINT HOW DID I FORGET
    ## my physics teacher can never see this mistake
    force = (((1000 * c1_mass * c2_mass) / distance**2))
    
    #calculating the acceleration of the planets using f = ma
    c1_a = force/c1_mass
    c2_a = force/c2_mass
    
    #print(((((c1_v[0]) ** 2) - ((c1_u[0]) ** 2))/(2 * c1_a), (((c1_v[1]) ** 2) - ((c1_u[1]) ** 2))/(2 * c1_a)))
<<<<<<< Updated upstream


    s = ((((c1_v[0]) ** 2) - ((c1_u[0]) ** 2))/(2 * c1_a), (((c1_v[1]) ** 2) - ((c1_u[1]) ** 2))/(2 * c1_a)) 
    #print(s)
=======
>>>>>>> Stashed changes
    
    #velocity formula to find the displacement v^2 - u^2 = 2as
    #calculates the displacemnt in terms of x,y
    c1_s = ((((c1_v[0]) ** 2) - ((c1_u[0]) ** 2))/(2 * c1_a), (((c1_v[1]) ** 2) - ((c1_u[1]) ** 2))/(2 * c1_a))
    ##this is the exact same as the line above but whatevs
    ##i hope you actually read these comments
    c2_s = ((((c2_v[0]) ** 2) - ((c2_u[0]) ** 2))/(2 * c2_a), (((c2_v[1]) ** 2) - ((c2_u[1]) ** 2))/(2 * c2_a))
    

    #print ('f: ', force)
    #print (c1_s, c2_s)
    
    if c1_s[1] > 5: #is 5 random or does it have meaning
        c1_s = 2 #same with 2???
    if c2_s[1] > 5:
        c2_s = 2
    
    #changes the position of the planets using the calculations above
    c1_pos[0] += int(c1_s[0])
    c1_pos[1] += int(c1_s[1])
    c2_pos[0] += int(c2_s[0])
    c2_pos[1] += int(c2_s[1])

    print(c1_pos[0])
    print(c1_pos[1])
    print(c2_pos[0])
    print(c2_pos[1])
    print()


c1_u = resolve(0, 0)
c2_u = resolve(10, math.pi/2)

c1_v = resolve(0, 0)
c2_v = resolve(0, 0)

c1_mass = 5
c2_mass = 15

colours = [(255, 0, 0), (0, 0, 255)]

win_loop = True
while win_loop:
    #makes the screen blank with two planets in their initial position
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