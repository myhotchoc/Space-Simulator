
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 15:32:45 2020
@author: Danny and Jenni (but he smells)
"""

import pygame
import random
import math
import time

## All data in metres
mercury_to_sun = 64956000000
venus_to_sun = 108660000000
earth_to_sun = 151840000000
mars_to_sun = 211250000000
jupiter_to_sun = 773770000000
saturn_to_sun = 1495600000000
uranus_to_sun = 2961800000000
neptune_to_sun = 4476700000000

## All data in kg
mercury_mass = 328500000000000000000000
venus_mass = 4867000000000000000000000
earth_mass = 5972000000000000000000000
mars_mass = 639000000000000000000000
jupiter_mass = 1898000000000000000000000000
saturn_mass = 568300000000000000000000000
uranus_mass = 86810000000000000000000000
neptune_mass = 102400000000000000000000000

## All data in metres
mercury_radius = 2438700
venus_radius = 6051800
earth_radius = 6371000
mars_radius = 3389500
jupiter_radius = 69911000
saturn_radius = 58232000
uranus_radius = 25362000
neptune_radius = 24622000

planet_data = [mercury_to_sun, venus_to_sun, earth_to_sun, mars_to_sun,
               jupiter_to_sun, saturn_to_sun, uranus_to_sun, neptune_to_sun,
               mercury_mass, venus_mass, earth_mass, mars_mass, jupiter_mass,
               saturn_mass, uranus_mass, neptune_mass, mercury_radius, venus_radius,
               earth_radius, mars_radius, jupiter_radius, saturn_radius,
               uranus_radius, neptune_radius]

ORANGE = (255, 128, 0) #FOR THE SUN
GREY = (128, 128, 128) #FOR MERCURY
BLOODORANGE = (255, 102, 0) #FOR VENUS
BLUE = (0, 128, 255) #FOR EARTH
DUST = (245, 202, 139) #FOR MARS
JUPITER_COL = (252, 91, 11) # COME UP WITH YOUR OWN NAME I HAVE NO CLUE
YELLOW = (242, 224, 63) #FOR SATURN
TURQUOISE = (125, 235, 224) #FOR UR ANUS
DARKBLUE = (19, 27, 246) #FOR NEPTUNE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Planet(object):
    def __init__(self, radius, orbital_dist, mass, colour, window, theta, theta1, number):
        self.radius = radius
        self.orbital_dist = orbital_dist
        self.mass = mass
        self.colour = colour
        self.window = window
        self.theta = theta
        self.theta1 = theta1
        self.number = number
        
        self.speed = (( (6.67408*(10**-1)) * self.mass/self.orbital_dist) ** 0.5)/100000


        
        #pygame.draw.circle(scree)
    
    def placePlanet(self):
        planet_pos = (centre[0], centre[1] - self.orbital_dist)
        
        self.planet = pygame.draw.circle(self.window, self.colour, planet_pos, self.radius)
        ##why is this self. and not just planet???  ## So I can access it outside the class definition or something innit
    
    def movePlanet(self, theta):
        self.theta += self.number 
        self.theta1 += self.number


        delta_x = int((((self.orbital_dist ) * math.cos(self.theta)) + centre[0]))
        delta_y = int((((self.orbital_dist ) * math.sin(self.theta1)) + centre[1]))
        #delta_y = int(centre[1] -self.orbital_dist + random.randint(5,8))
        
        planet_pos = (delta_x, delta_y)
        
        return planet_pos
        #pygame.blit(self.window, planet_pos)
        #pygame.draw.circle(self.window, self.colour, planet_pos, self.radius)

# Window size
win_size = (1000, 800)

#Screen object
screen = pygame.display.set_mode(win_size)

# Defining centre of screen
centre = (int(win_size[0]/2), int((win_size[1]/2)-70))
print(centre)

#Initialise window
pygame.init()


    

## Main window loop
game_loop = True
clock = pygame.time.Clock()

mercury = Planet(4, 70, mercury_mass, GREY, screen, 1, 1, 2.7)
mercury.placePlanet()

venus = Planet(8, 90, venus_mass, BLOODORANGE, screen, 1, 1, 1.9936)
venus.placePlanet()

earth = Planet(9, 110, earth_mass, BLUE, screen, 1, 1, 1.6974)
earth.placePlanet()

mars = Planet(5, 126, mars_mass, DUST, screen, 1, 1, 1.3727)
mars.placePlanet()

jupiter = Planet(20, 166, jupiter_mass, JUPITER_COL, screen, 1, 1, 0.7462)
jupiter.placePlanet()

saturn = Planet(16, 223, saturn_mass, YELLOW, screen, 1, 1, 0.5525)
saturn.placePlanet()

uranus = Planet(13, 306, uranus_mass, TURQUOISE, screen, 1, 1, 0.3873)
uranus.placePlanet()

neptune = Planet(12, 423, neptune_mass, DARKBLUE, screen, 1, 1, 0.3076)
neptune.placePlanet()

planets = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

# ''' Mercury 47.4 km/s
# Venus 35.0 km/s
# Earth 29.8 km/s
# Mars 24.1 km/s
# Jupiter 13.1 km/s
# Saturn 9.7 km/s
# Uranus 6.8 km/s
# Neptune 5.4 km/s '''

theta = 0

while game_loop:
    
    # Black background
    screen.fill(BLACK)
    
    ## (window, colour, position, radius)
    sun = pygame.draw.circle(screen, ORANGE, centre, 50)
    
    ##planet=(r, orbit_r, col, speed, window)
    
    # Gets list of all events
    for item in pygame.event.get():
        ## Quits loop if close button pressed
        
        if item.type == pygame.QUIT:
            game_loop = False
        
# =============================================================================
#         if item.type == pygame.MOUSEBUTTONUP:
#             
#             for theta in range(360):
#                 for i in planets:
#                     #pygame.draw.circle(screen, i.colour, new_pos, i.radius)
#                     new_pos = i.movePlanet(math.radians(theta))
#                     pygame.draw.circle(screen, i.colour, new_pos, i.radius)
#                     
#                 time.sleep(0.01)
#                 pygame.display.flip()
#                 clock.tick(60)
# =============================================================================
            
    #
    #ellipse1 = pygame.draw.ellipse(screen, WHITE, [430,370,130,130], 3)
    for i in planets:
        new_pos = i.movePlanet(math.radians(theta))
        pygame.draw.circle(screen, i.colour, new_pos, i.radius)
        #pygame.display.flip()
        #this stopped the planets like flashing idk if this is right now?
        #clock.tick(60)
        
    theta += 1
    
    # Update Screen, set framerate
    pygame.display.flip()
    clock.tick(30)

# Exit
pygame.quit()