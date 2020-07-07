# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 02:49:27 2020

@author: Danny
"""

import pygame, sys, math, random

## Colours
RED = [255, 0, 0, 255]
GREEN = [0, 255, 0, 255]
BLUE = [0, 0, 255, 255]
ORANGE = [255, 128, 0, 255]
YELLOW = [242, 224, 63, 255]
BLACK = [0, 0, 0, 255]
WHITE = [255, 255, 255, 255]
LIGHT_BLUE = [0,  255, 255, 255]
PINK = [255, 153, 255, 255]
LIME = [128, 255, 0, 255]

## Toggles pendulum smoke effects
smoke = True

## Constants
g = 0.2
vel_limit = 20
acc_val = 0.2

framerate = 60

v_lim = 3 ## Speed of smoke particles

particle_num = 7  ## Particles emitted per frame
offset = 20 ## Random force making particles move randomly
particle_size = 180 ## Size of each particle
decay_speed = 7 ## Time for particle to decay

p1_size = 40 ## Pendulum bob sizes
p2_size = 40

p1_length = 400 ## Pendulum lengths
p2_length = 300

p1_ang = math.pi/2 ## Pendulum starting angles
p2_ang = math.pi/12

p1_colour = RED ## Smoke colours
p2_colour = LIGHT_BLUE

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

## Pendulum object
class Pendulum(object):
    def __init__(self, size, colour, origin, theta, length, angVel, angAcc, damping):
        self.size = size
        self.colour = colour
        
        self.originx = origin[0]
        self.originy = origin[1]
        
        self.theta = theta
        self.length = length
        
        self.angVel = angVel
        self.angAcc = angAcc
        
        self.grav_force = 0.01
        self.damping = damping
        
        self.x = int(self.length * math.sin(self.theta)) + self.originx
        self.y = -int(self.length * math.cos(self.theta)) + self.originy
    
    def changePos(self):
        
        self.prev_x = self.x
        self.prev_y = self.y
        
        self.x = int(self.length * math.sin(self.theta)) + self.originx
        self.y = -int(self.length * math.cos(self.theta)) + self.originy

    
    def drawBody(self):
        pygame.draw.line(screen, WHITE, (self.originx, self.originy),
                         (self.x, self.y), 2)
        
        
    
    def changeAng(self):
        self.theta += self.angVel
    
    def changeAngVel(self):
        self.angVel += self.angAcc
    
    def drawBob(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size)
    
    def trace(self):
        pygame.draw.line(screen, WHITE, (self.x, self.y),
                         (self.prev_x, self.prev_y),
                         2)
    
    def go(self):
        self.changePos()
        
        self.changeAngVel()
        self.changeAng()
        
        self.drawBody()
        self.drawBob()
        
        self.angAcc = self.grav_force * math.sin(self.theta) / self.length * 100
        self.angVel = (self.angVel * self.damping)
     
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
        
    ## Changes colour of particle - decrements RGB values
    def fade(self):
        for r in range(len(self.col)):
            #print (r, particle.col[r])
            if self.col[r] > decay_speed:
                self.col[r] = self.col[r] - decay_speed
            else:
                self.col[r] = decay_speed


## Setting window size, defining screen
win_size = (1200, 1200)
screen = pygame.display.set_mode(win_size)

## Defining centre of screen
centre = (int(win_size[0]/2), int(win_size[1]/2))

## Initialise window
pygame.init()

## Defining clock object
clock = pygame.time.Clock()

#(size, col, origin, angle, length, vel, acc, damping)
p1 = Pendulum(p1_size, p1_colour,
                 (centre[0], 200),
                 p1_ang, p1_length,
                 0, 0, 1)

p1.changePos()

p2 = Pendulum(p2_size, p2_colour,
              (p1.x, p1.y),
              p2_ang, p2_length,
              0, 0, 1)


pendulums = [p1]

particles = []

## Window runtime loop
win_loop = True
while win_loop:
    ## Refills background
    screen.fill(BLACK)
    
    ## Checks for QUIT event to break loop
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            win_loop = False
    
    #pygame.draw.circle(screen, WHITE, (p1.originx, p1.originy), 15)
    
    for p in pendulums:
        p.go()
        
        
    p2.originx, p2.originy = p.x, p.y
    p2.go()
    
    if smoke == True:
        for i in range(particle_num):
    
        
            p = Particle([p1_colour[0], p1_colour[1], p1_colour[2]],
                         particle_size, (p2.x, p2.y),
                     (random.uniform(-v_lim, v_lim), random.uniform(-v_lim, 1.5)),
                     (0, 0),
                     (0, 0),
                     255)
            particles.append(p)
            
            p = Particle([p2_colour[0], p2_colour[1], p2_colour[2]],
                         particle_size, (p1.x, p1.y),
                     (random.uniform(-v_lim, v_lim), random.uniform(-v_lim, 1.5)),
                     (0, 0),
                     (0, 0),
                     255)
            particles.append(p)
        
        ## Iterating over all Particle objects on screen
        for i in particles:
            ## Set current acceleration, force to zero
            i.ax, i.ay = 0, 0
            i.fx, i.fy = 0, 0
            
            #i.applyForce(i.weight)
            i.applyForce((random.uniform(-offset, offset), (random.uniform(-offset, offset))))
            
                
            #i.col = (0, 0, i.lifespan)
            
            
            ## Deincrement lifespan
            i.lifespan -= decay_speed
                 
            ## Run movement algorithm
            i.move()
            
            ## Draw particle to screen
            pygame.draw.circle(screen, i.col, (int(i.px), int(i.py)), i.radius)
            
            if i.lifespan <= 0:
                particles.remove(i)
            
            i.fade()
# =============================================================================
#         if i.col[0] > 0:
#             i.col[0] -= decay_speed
#         if i.col[2] > 0:
#             i.col[2] -= decay_speed
# =============================================================================
    
    ## Update screen
    pygame.display.flip()
    clock.tick(60)
    
## Close window
pygame.quit()
sys.exit()