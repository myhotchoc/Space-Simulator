# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 15:32:45 2020

@author: Danny and Jenni (but he smells)
"""

import pygame
import random

# Defining colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)
BLUE = (0, 0, 255)
PURPLE = (238, 130, 238)

class Planet(object):
    def __init__(self, radius, orbital_dist, colour, speed, window):
        self.radius = radius
        self.orbital_dist = orbital_dist
        self.colour = colour
        self.speed = speed
        self.window = window
        
        #pygame.draw.circle(scree)
    
    def placePlanet(self):
        
        planet_pos = (centre[0], centre[1] - self.orbital_dist)
        
        pygame.draw.circle(self.window, self.colour, planet_pos, self.radius)

# Window size
win_size = (1000, 1000)

#Screen object
screen = pygame.display.set_mode(win_size)

# Defining centre of screen
centre = (int(win_size[0]/2), int(win_size[1]/2))

#Initialise window
pygame.init()

## Main window loop
game_loop = True
clock = pygame.time.Clock()

while game_loop:
    
    # Gets list of all events
    for item in pygame.event.get():
        ## Quits loop if close button pressed
        
        if item.type == pygame.QUIT:
            game_loop = False
        
        if item.type == pygame.MOUSEBUTTONUP:
            p1 = Planet(50, 1, RED, 10, screen)
            p1.placePlanet()
        
            
    # Black background, white circle in centre
    screen.fill(BLACK)
    
    ## (win, col, pos, r)
    sun = pygame.draw.circle(screen, YELLOW, centre, 40)
    
    p1 = Planet(10, 60, RED, 10, screen)
    p1.placePlanet()
    
    p2 = Planet(15, 120, GREEN, 10, screen)
    p2.placePlanet()
    
    p3 = Planet(10, 190, BLUE, 10, screen)
    p3.placePlanet()
    
    p4 = Planet(20, 250, PURPLE, 10, screen)
    p4.placePlanet()

    
    #ellipse1 = pygame.draw.ellipse(screen, WHITE, [100,100,800,300], 3)
    
    # Update Screen, set framerate
    pygame.display.flip()
    clock.tick(60)

# Exit
pygame.quit()
