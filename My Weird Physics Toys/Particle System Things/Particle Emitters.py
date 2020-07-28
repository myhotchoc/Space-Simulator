import pygame
import math
import random
import sys

## Press R to make a repeller, space to turn off gravity, arrow keys for wind

## Colours
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
ORANGE = [255, 128, 0]
YELLOW = [242, 224, 63]
BLACK = [0, 0, 0, 255]
WHITE = [255, 255, 255]
LIGHT_BLUE = [0,  255, 255]
PINK = [255, 153, 255]
LIME = [150, 255, 0]

## Constants

bounce = False
gravity = True
particleFade = True
windLeft = False
windRight = False

wind_right_force = (2.5, 0)
wind_left_force = (-2.5, 0)

g = 0.1  ## acceleration due to gravity
radius_constant = 3
framerate = 120 ## frames per second

v_lim = 0.5 ## max velocity of particles
f_limit = 5

particle_num = 1 ## Particles created per system
offset = 3 ## Maximum offset particle is moved by
particle_size = 15 ## size of particles
decay_speed = 1.7 ## speed of decay
lifespan = 255

repel_mass = 50
repeller_strength = 40

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

def distance(body1, body2):
    ## Difference in x-pos and y-pos
    delta_x = body2.px - body1.px
    delta_y = body2.py - body1.py
    
    ## Uses Pythagorean Theorem
    return math.sqrt((delta_x)**2 + (delta_y)**2)

## Single Particle object
## (colour, mass, pos, vel, acc, force, lifespan)
class Particle(object):
    def __init__(self, col, mass, p, v, a, f, lifespan):
        self.col = col
        self.mass = mass
        
        ## Radius of circle is proportional to sqrt of mass (S.A = kr^2)
        self.radius = int(math.sqrt(mass) * radius_constant)
        
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
        
        self.prevPos = (0, 0)
    
    ## Adds velocity to position
    def changePos(self):
        
        self.prevPos = (self.px, self.py)
        
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
        if bounce == True:
            self.bounce()
        
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
    
    def replacePrevPos(self):
        pygame.draw.circle(screen, BLACK, self.prevPos, self.radius)
    
class Repeller(Particle):
    def __init__(self, G, p):
        self.G = G
        self.px = p[0]
        self.py = p[1]
        
        super().__init__(WHITE, repel_mass, p, (0, 0), (0, 0), (0, 0), 0)
        
    def repel(self, body):
        r = distance(self, body)
        dir_x, dir_y = unitVector((self.px - body.px), (self.py-body.py))
        
        if r != 0:
            strength = self.G * (self.mass * body.mass) / r**2
        else:
            strength = 75
        
        fx, fy = setMag(dir_x, dir_y, strength)
        
        fx, fy = limit(fx, fy, f_limit)
        
        body.fx += fx
        body.fy += fy

## Particle system class
class ParticleSystem(object):
    ## Takes origin of particles, colour
    def __init__(self, origin, c):
        self.origin = origin
        ## List of all Particle objects in system
        self.particles = []
        self.c = c
        self.positions = []
    
    ## Method to generate Particle objects
    def makeEmitter(self):
        
        ## Makes particle_num Particle objects
        for j in range(particle_num):
    
            ## Generate new object with appropriate attributes, random initial velocity
            p = Particle([self.c[0], self.c[1], self.c[2]],
                         particle_size, self.origin,
                     (random.uniform(-v_lim, 3*v_lim), random.uniform(-v_lim, 3*v_lim)),
                     (0, 0),
                     (0, 0),
                     lifespan)
            ## Adds new particle to list of all particles in system
            self.particles.append(p)
            
    ## Method to move and update the system
    def moveParticles(self):

        ## Iterating over all Particle objects in system
        for particle in self.particles:
            
            ## Set current acceleration, force to zero
            particle.ax, particle.ay = 0, 0
            
            
            ## Apply weight force, random offset force
            if gravity == True:
                particle.applyForce(particle.weight)
                
                
            particle.applyForce((random.uniform(-offset, offset), (random.uniform(-offset, offset))))
            
            ## Deincrement lifespan
            particle.lifespan -= decay_speed
                 
            ## Run movement algorithm
            particle.move()
            
            ## Draw particle to screen
            pygame.draw.circle(screen, particle.col, (int(particle.px), int(particle.py)), particle.radius)
            
            ## Check if particle is still alive
            if particle.isAlive() == False:
                ## If particle is dead, remove from particle list
                self.particles.remove(particle)
            
            self.positions.append((particle.px, particle.py))
            
            ## Changes colour (fading affect)
            if particleFade == True:
                particle.fade()
            
            particle.fx, particle.fy = 0, 0

    def finished(self):
        if len(self.particles) == 0:
            return True
        else:
            return False
    
    def applyForce(self, force):
        for i in self.particles:
            i.applyForce(force)
    
    def repel(self):
        for repeller in repellers:
            for p in self.particles:
                repeller.repel(p)

## Get mouse position
mouse = pygame.mouse.get_pos()

## Initialise empty systems array to hold all particle systems
systems = []
repellers = []

## Fill screen with black
screen.fill(BLACK)

## Main runtime loop
while win_loop:
    
    ## Refills background
    screen.fill(BLACK)
    
    ## Getting coordinates of mouse position
    mouse = pygame.mouse.get_pos()
    
    ## Iterates over all events
    for i in pygame.event.get():
        
        ## Checks for QUIT event to break loop
        if i.type == pygame.QUIT:
            win_loop = False
        
        ## Checks for mouse click to make new particle system
        if i.type == pygame.MOUSEBUTTONDOWN:
            
            ## Create random colour
            p = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
            
            ## Create new ParticleSystem object, origin=mouse position and col = random colour
            system = ParticleSystem(mouse, p)
            ## Generate particle objects at origin with makeEmitter method
            system.makeEmitter()
            
            ## Add new Particle system to list of all systems
            systems.append(system)
    
        
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_RIGHT:
                windRight = True                
            if i.key == pygame.K_LEFT:
                windLeft = True
            if i.key == pygame.K_SPACE:
                gravity = False
            
            if i.key == pygame.K_r:
                r = Repeller(repeller_strength, mouse)
                repellers.append(r)
        
        if i.type == pygame.KEYUP:
            if i.key == pygame.K_RIGHT:
                windRight = False
            if i.key == pygame.K_LEFT:
                windLeft = False
        
            else:
                gravity = True
    
                
                
        
    ## Iterate over all systems
    for system in systems:
        ## Generate particle objects at origin with makeEmitter method
        system.makeEmitter()
        
        if windRight == True:
            system.applyForce(wind_right_force)
        if windLeft == True:
            system.applyForce(wind_left_force)
        
        system.repel()
        
        ## Move and update all particle objects in system
        system.moveParticles()
    
    for repeller in repellers:
        pygame.draw.circle(screen, repeller.col, (int(repeller.px), int(repeller.py)), repeller.radius)


    ## Update screen
    pygame.display.flip()
    clock.tick(framerate)
    
## Close window
pygame.quit()
sys.exit()