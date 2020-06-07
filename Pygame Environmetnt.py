# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 15:32:45 2020

@author: Danny and Jenni
"""
import pygame

# Defining colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Window size
win_size = (500, 500)

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
            
    # Black background, white circle in centre
    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, centre, 10)
    
    # Update Screen, set framerate
    pygame.display.flip()
    clock.tick(60)

# Exit
pygame.quit()
