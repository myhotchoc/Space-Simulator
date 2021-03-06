# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 01:49:55 2020

@author: Danny
"""
import math
import pygame

## RGB values for colours
ORANGE = (255, 128, 0)
GREY = (128, 128, 128)
BLOODORANGE = (255, 102, 0)
BLUE = (0, 128, 255)
DUST = (245, 202, 139)
JUPITER_COL = (252, 91, 11)
YELLOW = (242, 224, 63)
TURQUOISE = (125, 235, 224)
DARKBLUE = (19, 27, 246)
BLACK = (0, 0, 0)

## Newton's Gravitational Constant but I changed the value 
G = 50

mercury_col = GREY
venus_col = BLOODORANGE
earth_col = BLUE
mars_col = DUST
jupiter_col = JUPITER_COL
saturn_col = YELLOW
uranus_col = TURQUOISE
neptune_col = DARKBLUE

## All data in metres
mercury_to_sun = 50
venus_to_sun = 75
earth_to_sun = 105
mars_to_sun = 125
jupiter_to_sun = 190
saturn_to_sun = 260
uranus_to_sun = 330
neptune_to_sun = 400

## All data in kg
sun_mass = 50
mercury_mass = 3
venus_mass = 5
earth_mass = 5
mars_mass = 6
jupiter_mass = 37
saturn_mass = 28
uranus_mass = 20
neptune_mass = 25

## All data in metres
sun_radius = 30
mercury_radius = 4
venus_radius = 7
earth_radius = 8
mars_radius = 7
jupiter_radius = 16
saturn_radius = 14
uranus_radius = 12
neptune_radius = 13

## Initial speeds
mercury_speed = 7
venus_speed = 6
earth_speed = 5
mars_speed = 4.6
jupiter_speed = 3.5
saturn_speed = 3
uranus_speed = 2.8
neptune_speed = 2.5

timestep = 0.5

## Class for a body in space
class Body(object):
    ## mass, x-position, y-position, x-velocity, y-velocity, colour, radius
    def __init__(self, mass, px, py, vx, vy, colour, radius):
        self.mass = mass
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.colour = colour
        self.radius = int(math.sqrt(mass)) * 3
        
        ## Holds all past locations
        self.past = []
    
    ## Returns distance between two bodies
    def distance(self, body2):
        ## Difference in x-pos and y-pos
        delta_x = body2.px - self.px
        delta_y = body2.py - self.py
        
        ## Uses Pythagorean Theorem
        return math.sqrt((delta_x)**2 + (delta_y)**2)
    
    ## Defines force between two bodies
    def force(self, body2):
        
        ## Newton's Law of Gravitation - F=G*m1*m2/r^2
        f = (G * self.mass * body2.mass) / (self.distance(body2) ** 2)
        
        ## Difference in x-pos and y-pos
        delta_x = body2.px - self.px
        delta_y = body2.py - self.py
        
        ## Angle between bodies
        theta = math.atan2(delta_y, delta_x)
        
        ## Resolves forces to get x and y components of force
        self.fx = f * math.cos(theta)
        self.fy = f * math.sin(theta)

    ## Updates position and velocity of body
    def changePos(self):
        
        ## F=ma --> a = F/m
        ## Adding acceleration to current velocity
        ## v = u + a*t
        self.vx += self.fx/self.mass * timestep
        self.vy += self.fy/self.mass * timestep
        
        ## Makes bodies 'bounce' off walls if they reach walls
        ## Reverses velocity if position is greater than size, or less than 0
        if self.px + self.vx >= win_size[0] or self.px + self.vx <= 0:
            self.vx = -self.vx
            
        if self.py + self.vy >= win_size[1] or self.py + self.vy <= 0:
            self.vy = -self.vy
        
        ## Adds velocity to current position
        self.py += self.vy * timestep
        self.px += self.vx * timestep
        
        ## Adds current position to list of all positions
        ## Comment me out to stop the planet trails
        self.past.append([self.px, self.py])
            
    
    
## Setting window size, defining screen
win_size = (900, 900)
screen = pygame.display.set_mode(win_size)

## Defining centre of screen
centre = (int(win_size[0]/2), int(win_size[1]/2))

## Initialise window
pygame.init()

## Defining clock object
clock = pygame.time.Clock()

## Window runtime loop variable
win_loop = True

## Defining Solar System bodies
sun = Body(sun_mass, centre[0], centre[1], 0, 0, ORANGE, sun_radius)

mercury = Body(mercury_mass, centre[0], centre[1]+mercury_to_sun, mercury_speed, 0, mercury_col, mercury_radius)
venus = Body(venus_mass, centre[0], centre[1]+venus_to_sun, -venus_speed, 0, venus_col, venus_radius)
earth = Body(earth_mass, centre[0], centre[1]+earth_to_sun, earth_speed, 0, earth_col, earth_radius)
mars = Body(mars_mass, centre[0], centre[1]+mars_to_sun, mars_speed, 0, mars_col, mars_radius)
jupiter = Body(jupiter_mass, centre[0], centre[1]+jupiter_to_sun, jupiter_speed, 0, jupiter_col, jupiter_radius)
saturn = Body(saturn_mass, centre[0], centre[1]+saturn_to_sun, saturn_speed, 0, saturn_col, saturn_radius)
uranus = Body(uranus_mass, centre[0], centre[1]+uranus_to_sun, uranus_speed, 0, uranus_col, uranus_radius)
neptune = Body(neptune_mass, centre[0], centre[1]+neptune_to_sun, neptune_speed, 0, neptune_col, neptune_radius)

## List of all planets
planets = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

gravity = True

## Main runtime loop
while win_loop:
    
    ## Refills background with black
    screen.fill((0, 0, 0))
    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False
            
        if i.type == pygame.MOUSEBUTTONDOWN:
            gravity = False
        
        if i.type == pygame.MOUSEBUTTONUP:
            gravity = True
    
    ## Draw sun
    pygame.draw.circle(screen, sun.colour, (int(sun.px), int(sun.py)), sun_radius)
    
    ## Iterate through each planet
    for i in planets:
        ## Draws dot at each past position
        for j in i.past:
            pygame.draw.circle(screen, i.colour, (int(j[0]), int(j[1])), 0)
        
        ## Draw planet at current position
        pygame.draw.circle(screen, i.colour, (int(i.px), int(i.py)), i.radius)
        ## Calculate force on planet due to the sun
        
        if gravity == True:
            i.force(sun)
            
        ## Update velocity and position data
        i.changePos()

    ## Update screen
    pygame.display.flip()
    clock.tick(60)
    
## Close window
pygame.quit()
