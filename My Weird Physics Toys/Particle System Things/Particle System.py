# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 09:35:40 2020

@author: Danny
"""

import pygame
import math
import random
import sys

## Defining colours
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
ORANGE = [255, 128, 0]
YELLOW = [242, 224, 63]
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]


## Constants
g = 0.1
vel_limit = 5
acc_val = 0.2
framerate = 60
v_lim = 2
particle_num = 50
offset = 2
particle_size = 6
decay_speed = 4

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

## Return magnitude, direction of a given vector
def magDir(x, y):
    return math.sqrt(x**2 + y**2), round(math.atan2(y, x), 5)

## Return x, y components of given vector
def resolve(mag, t):
    return mag*math.cos(t), mag*math.sin(t)

## Return direction of given vector
def direction(x, y):
    return math.atan2(y, x)

## Return magnitude of given vector
def mag(x, y):
    return math.sqrt(x**2 + y**2)

## Scale given vector to given magnitude
def setMag(x, y, m):
    
    magnitude = mag(x, y)
    
    if magnitude == 0:
        return 0, 0
    else:
    
        x = x/magnitude * m
        y = y/magnitude * m
    
    return x, y

## Scale given vector to unit length
def unitVector(x, y):
    x, y = setMag(x, y, 1)
    
    return x, y

## Limit given vector to given max length
def limit(x, y, a):
    if mag(x, y) >= a:
        x, y = setMag(x, y, a)
        
    return x, y


## Single Particle object
## (colour, mass, pos, vel, acc, force, lifespan)
class Particle(object):
    def __init__(self, col, mass, p, v, a, f, lifespan):
        self.col = col
        self.mass = mass
        
        ## Radius of circle is proportional to sqrt of mass (S.A = kr^2)
        self.radius = int(math.sqrt(mass) * 3)
        
        ## Components of pos, vel, acc, force
        self.px = p[0]
        self.py = p[1]
        
        self.vx = v[0]
        self.vy = v[1]
        
        self.ax = a[0]
        self.ay = a[1]
        
        self.fx = f[0]
        self.fy = f[1]
        
        ## Lifespan
        self.lifespan = lifespan
        
        ## Weight is vector with y-component f=ma=mg
        self.weight = [0, self.mass * g]
    
    ## Adds velocity to position
    def changePos(self):
        
        self.px = int(self.px + self.vx)
        self.py = int(self.py + self.vy)
    
    ## Adds acceleration to velocity
    def changeVel(self):
        self.vx += self.ax
        self.vy += self.ay
    
    ## f=ma --> new a = f/mass
    def changeAcc(self):
        
        self.ax += self.fx/self.mass
        self.ay += self.fy/self.mass

    
    ## Add given force to total (resultant) force
    def applyForce(self, force):
        self.fx += force[0]
        self.fy += force[1]
        #print (self.fy)
        
        ## Force arrow that doesn't work properly
        #drawArrow(screen, (100, 255, 0), (self.px, self.py),(self.px +force[0] , self.py+force[1]*0.1 ))
    
    ## Accelerate body to mouse location
    def moveToMouse(self, mouse):
        ## Figure out direction
        self.ax = mouse[0] - self.px
        self.ay = mouse[1] - self.py
        
        ## Set magnitude to value of acceleration (constant at the top)
        self.ax, self.ay = setMag(self.ax, self.ay, acc_val)
        
        ## Change the velocity, limit to constant
        self.changeVel()
        self.vx, self.vy = limit(self.vx, self.vy, vel_limit)
        
        ## Change position
        self.changePos()
    
    ## Bounce off walls of screen
    def bounce(self):
        if self.px + self.vx >= win_size[0] or self.px + self.vx < 0:
            self.vx = -self.vx
            
        if self.py + self.vy >= win_size[1] or self.py + self.vy < 0:
            self.vy = -self.vy
    
    ## Check if still alive (using lifespan value)
    def isAlive(self):
        if self.lifespan <= 0:
            return False
        else:
            return True
        
    
    ## Full movement algorithm
    def move(self):          
        ## Accelerate to mouse location
        #self.moveToMouse(mouse)
        
        ## Bounce of screen edge
        #self.bounce()
        
        ## Change acceleration
        self.changeAcc()
        #i.ax, i.ay = limit(i.ax, i.ay, acc_val)
        
        ## Change velocity
        self.changeVel()
        #i.vx, i.vy = limit(i.vx, i.vy, vel_limit)
        
        ## Change position
        self.changePos()

class ParticleSystem(object):
    def __init__(self, origin, c):
        self.origin = origin
        self.particles = []
        self.c = c
    
    def makeEmitter(self):
        rand_col = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        #c = [255, 100, 50]
        for j in range(particle_num):
    
            p = Particle([self.c[0], self.c[1], self.c[2]],
                         particle_size, self.origin,
                     (random.uniform(-v_lim, v_lim), random.uniform(-v_lim, 1.5)),
                     (0, 0),
                     (0, 0),
                     255)
            self.particles.append(p)
            
    
    def moveParticles(self):
        ## Iterating over all Particle objects on screen
        for particle in self.particles:
            ## Set current acceleration, force to zero
            particle.ax, particle.ay = 0, 0
            particle.fx, particle.fy = 0, 0
            
            #particle.applyForce(particle.weight)
            particle.applyForce((random.uniform(-offset, offset), (random.uniform(-offset, offset))))
            
            ## Deincrement lifespan
            particle.lifespan -= decay_speed
                 
            ## Run movement algorithm
            particle.move()
            
            ## Draw particle to screen
            pygame.draw.circle(screen, particle.col, (int(particle.px), int(particle.py)), particle.radius)
            
            if particle.lifespan <= 0:
                self.particles.remove(particle)
                
            for r in range(len(particle.col)):
                #print (r, particle.col[r])
                if particle.col[r] > decay_speed:
                    particle.col[r] = particle.col[r] - 1
                else:
                    particle.col[r] = 0




## Defining Particle object
## (col, mass, pos, vel, acc, force, lifespan)

mouse = pygame.mouse.get_pos()
systems = []
screen.fill(BLACK)
## Main runtime loop
while win_loop:
    ## Refills background
    #screen.fill((0, 0, 0))
    

    ## Getting coordinates of mouse position
    mouse = pygame.mouse.get_pos()
    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False
        
        if i.type == pygame.MOUSEBUTTONDOWN:
            p = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
            system = ParticleSystem(mouse, p)
            system.makeEmitter()
            
            systems.append(system)
        
            
    for system in systems:
        system.moveParticles()


    ## Update screen
    pygame.display.flip()
    clock.tick(framerate)
    
## Close window
pygame.quit()
sys.exit()