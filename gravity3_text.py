# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 01:49:55 2020

@author: Danny and Jenni
"""
import math
import pygame
import tkinter as tk
from tkinter import messagebox

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
saturn_to_sun = 240
uranus_to_sun = 300
neptune_to_sun = 380

## All data in kg
sun_mass = 50
mercury_mass = 3
venus_mass = 5
earth_mass = 5
mars_mass = 6
jupiter_mass = 35
saturn_mass = 32
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

timestep = 1
win_size = (900, 900)
planets_array = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
data_array =  []

#opens the file and adds all the data to an array 
file = open("planet_data.txt", "r")
for line in file:
    y = line.split()
    data_array.append(y)
file.close()

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
        self.radius = radius
        
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
    

root = tk.Tk()
root.title("Planets")
title = tk.Label(root, text = 'Choose which planets you want:')
title.grid(row= 0, column = 0)
#creates a list of the avaliable planets to be shown on the pygame interface
planets_selection = tk.Listbox(root, selectmode = 'multiple', height = 8 )
for item in planets_array:
    planets_selection.insert(tk.END, item)
planets_selection.grid(row = 1, column = 0)

#produces a list of the indices of the planets selected - starting from zero



def solarSystem(): 
    planetsChosen = planets_selection.curselection()  
    ## Setting window size, defining screen
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
    marsBut = pygame.Rect(100,100,50,50)

    planets = []
    planets_chosen = list(planetsChosen)
    if 0 in planets_chosen:
        mercury = Body(mercury_mass, centre[0], centre[1]+mercury_to_sun, mercury_speed, 0, mercury_col, mercury_radius)
        planets.append(mercury)
    if 1 in planets_chosen:
        venus = Body(venus_mass, centre[0], centre[1]+venus_to_sun, -venus_speed, 0, venus_col, venus_radius)
        planets.append(venus)
    if 2 in planets_chosen:
        earth = Body(earth_mass, centre[0], centre[1]+earth_to_sun, earth_speed, 0, earth_col, earth_radius)
        planets.append(earth)
    if 3 in planets_chosen:
        mars = Body(mars_mass, centre[0], centre[1]+mars_to_sun, mars_speed, 0, mars_col, mars_radius)
        planets.append(mars)
    if 4 in planets_chosen:
        jupiter = Body(jupiter_mass, centre[0], centre[1]+jupiter_to_sun, jupiter_speed, 0, jupiter_col, jupiter_radius)
        planets.append(jupiter)
    if 5 in planets_chosen:
        saturn = Body(saturn_mass, centre[0], centre[1]+saturn_to_sun, saturn_speed, 0, saturn_col, saturn_radius)
        planets.append(saturn)
    if 6 in planets_chosen:
        uranus = Body(uranus_mass, centre[0], centre[1]+uranus_to_sun, uranus_speed, 0, uranus_col, uranus_radius)
        planets.append(uranus)
    if 7 in planets_chosen:
        neptune = Body(neptune_mass, centre[0], centre[1]+neptune_to_sun, neptune_speed, 0, neptune_col, neptune_radius)
        planets.append(neptune)

    ## List of all planets
    #planets = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
    gravity = True

    ## Main runtime loop
    while win_loop:
        ## Refills background with black
        screen.fill((0, 0, 0))
        
        ## Checks for QUIT event to break loop
        for i in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if i.type == pygame.QUIT:
                win_loop = False
                
            if i.type == pygame.MOUSEBUTTONDOWN:
                if marsBut.collidepoint(mouse_pos):
                    messagebox.showinfo('HEY')
                else:
                    gravity = False
            
            if i.type == pygame.MOUSEBUTTONUP:
                gravity = True
            
        
        ## Draw sun
        pygame.draw.circle(screen, sun.colour, (int(sun.px), int(sun.py)), sun_radius)
        
        ## Iterate through each planet
        for i in planets:
            ## Draws dot at each past position
            for j in i.past:
                pygame.draw.circle(screen, i.colour, (int(j[0]), int(j[1])), 1)
            
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

#prints the data for the selected planet
def PrintInfo(p,q, planet):
    baseFrame = tk.Toplevel(base)
    baseFrame.title(planet)
    quote1 = "The distance from " + planet + " to the Sun is: " + data_array[p][2] + " in metres." 
    quote2 = "The mass of " + planet + " is: " + data_array[p+1][2] + " in kg."
    quote3 = "The radius of " + planet + " is:" + data_array[q][2] + " in metres."
    quote = quote1 + "\n" + quote2 + "\n" + quote3
    data = tk.Text(baseFrame)
    data.insert(tk.END, quote)
    data.pack()


#creates the layout on the interface
def createInfoInterface(base):
    merc = tk.Button(base, text = "Mercury", command = lambda: PrintInfo(1, 4, "Mercury"),bg = "grey1", fg = 'grey69' )
    merc.grid(row = 1, column = 1,)
    star3 = tk.Label(base, height = 1, width = 6, bg = 'black')
    star3.grid(row=2, column = 0)
    space = tk.Label(base, height = 1, width = 6, bg = "black")
    space.grid(row=1, column = 2)
    ven = tk.Button(base, text = "Venus", command = lambda: PrintInfo(4, 7, "Venus"), fg = 'orange red')
    ven.grid(row=1, column = 3)
    star = tk.Label(base, height = 1, width = 1, bg = 'black')
    star.grid(row=2, column = 0)
    space1 = tk.Label(base, height = 1, width = 6, bg = "black")
    space1.grid(row=3, column = 2)
    ear = tk.Button(base, text = "Earth", command = lambda: PrintInfo(7, 10, "Earth"), fg = 'seagreen3')
    ear.grid(row=3, column = 1)
    star5 = tk.Label(base, height = 1, width = 6, bg = 'black')
    star5.grid(row=3, column = 0)
    mar = tk.Button(base, text = "Mars", command = lambda: PrintInfo(10, 13, "Mars"), fg = 'light salmon')
    mar.grid(row=3, column = 3)
    star1 = tk.Label(base, height = 1, width = 1, bg = 'black')
    star1.grid(row=4, column = 0)
    jup = tk.Button(base, text = "Jupiter", command = lambda: PrintInfo(13, 16, "Jupiter"), fg = 'red3')
    jup.grid(row=5, column = 1)
    star6 = tk.Label(base, height = 1, width = 6, bg = 'black')
    star6.grid(row=5, column = 0)
    space3 = tk.Label(base, height = 1, width = 6, bg = "black")
    space3.grid(row=5, column = 2)
    sat = tk.Button(base, text = "Saturn", command = lambda: PrintInfo(16, 19, "Saturn"), fg = 'pale goldenrod')
    sat.grid(row=5, column = 3)
    star2 = tk.Label(base, height = 1, width = 1, bg = 'black')
    star2.grid(row=6, column = 0)
    ura = tk.Button(base, text = "Uranus", command = lambda: PrintInfo(19, 22, "Uranus"), fg = 'turquoise2')
    ura.grid(row=7, column = 1)
    star7 = tk.Label(base, height = 1, width = 6, bg = 'black')
    star7.grid(row=7, column = 0)
    space4 = tk.Label(base, height = 1, width = 6, bg = "black")
    space4.grid(row=7, column = 2)
    nep = tk.Button(base, text = "Neptune", command = lambda: PrintInfo(22, 24, "Neptune"), fg = 'blue')
    nep.grid(row=7, column = 3)
    space5 = tk.Label(base, height = 1, width = 6, bg = "black")
    space5.grid(row=8, column = 2)
    endspace = tk.Label(base, height = 1, width = 6, bg = "black")
    endspace.grid(row=1, column = 4)


btn = tk.Button(root, text ='Done', command = lambda: solarSystem())
btn.grid(row = 2, column = 0)
       
base = tk.Tk()
base.title("Select a planet to view it's information")
base["bg"] = "black"
star4= tk.Label(base, height = 1, width = 1, bg = "black")
star4.grid(row=0, column = 1)
createInfoInterface(base)
base.mainloop()

root.mainloop()

## Close window
pygame.quit()
